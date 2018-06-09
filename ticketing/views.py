from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Avg

from .models import Cinema, Movie, Session, House, House_all, Order, Customer, Employee, Cinema_comment, Movie_comment
from .forms import MovieCommentForm, CinemaCommentForm
import time
import json

# Create your views here.


def check_log(func):
    def check_user(request, *args, **kwargs):
        email = request.session.get('email')
        if email:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/user/login')
    return check_user


def index(request):
    """学习笔记的主页"""
    if request.session.get('employee', False):
        employee = Employee.objects.get(username=request.user.get_username())
        cinema = employee.cinema_id
        context = {'cinema': cinema}
        return render(request, 'cinema_index.html', context)
    return render(request, 'index.html')


def movies(request):
    """显示所有的电影"""
    Movies = Movie.objects.order_by('-score')
    movie_scores = []
    for movie in Movies:
        item = {}
        item['movie_id'] = movie.movie_id
        item['director'] = movie.director
        item['name'] = movie.name
        item['type'] = movie.type
        item['length'] = movie.length
        comments = Movie_comment.objects.filter(movie_id=movie.movie_id)
        if len(comments) == 0:
            item['score'] = False
        else:
            item['score'] = comments.aggregate(avg_score=Avg('score'))['avg_score']
        movie_scores.append(item)
    context = {'movie_scores': movie_scores}
    # print(context)
    return render(request, 'movies.html', context)


def movie(request, movie_id):
    """显示电影对应的所有场次"""
    one_movie = Movie.objects.get(movie_id=movie_id)
    comments = Movie_comment.objects.filter(movie_id=movie_id)
    score = False
    if len(comments) > 0:
        score = comments.aggregate(avg_score=Avg('score'))['avg_score']
    cursor = connection.cursor()
    cursor.execute("SELECT session_id, ticketing_cinema.name, ticketing_movie.name, house_name, start_time, price "
                   "FROM ((ticketing_house join ticketing_session on ticketing_session.house_id_id = ticketing_house.house_id) "
                   "join ticketing_cinema on ticketing_house.cinema_id_id = ticketing_cinema.cinema_id) "
                   "join ticketing_movie on ticketing_session.movie_id_id = ticketing_movie.movie_id "
                   "where ticketing_movie.movie_id = %s order by start_time;", [movie_id])
    sessions = cursor.fetchall()
    Sessions = []
    for session in sessions:
        sess = {}
        sess['session_id'] = session[0]
        sess['cinema_name'] = session[1]
        sess['movie_name'] = session[2]
        sess['house_name'] = session[3]
        sess['start_time'] = session[4]
        sess['price'] = session[5]
        Sessions.append(sess)
    # 获取电影movie_id的所有的评价
    cursor.execute("select username_id, comment, score from ticketing_movie_comment where movie_id_id = %s;", [movie_id])
    comments = cursor.fetchall()
    Comments = []
    for comment in comments:
        com = {}
        com['username'] = comment[0]
        com['comment'] = comment[1]
        com['score'] = comment[2]
        Comments.append(com)
    context = {'sessions': Sessions, 'comments': Comments, 'movie': one_movie, 'score': score, 'cinema': False}
    return render(request, 'sessions.html', context)


def cinemas(request):
    """显示所有的影院"""
    Cinemas = Cinema.objects.order_by('-score')
    cinema_scores = []
    for cinema in Cinemas:
        item = {}
        item = {}
        item['cinema_id'] = cinema.cinema_id
        item['tel'] = cinema.tel
        item['name'] = cinema.name
        item['address'] = cinema.address
        comments = Cinema_comment.objects.filter(cinema_id=cinema.cinema_id)
        if len(comments) == 0:
            item['score'] = False
        else:
            item['score'] = comments.aggregate(avg_score=Avg('score'))['avg_score']
        cinema_scores.append(item)
    context = {'cinema_scores': cinema_scores}
    return render(request, 'cinemas.html', context)


def cinema(request, cinema_id):
    """显示影院对应的所有场次"""
    one_cinema = Cinema.objects.get(cinema_id=cinema_id)
    cursor = connection.cursor()
    cursor.execute("SELECT session_id, ticketing_cinema.name, ticketing_movie.name, house_name, start_time, price "
                   "FROM ((ticketing_house join ticketing_session on ticketing_session.house_id_id = ticketing_house.house_id) "
                   "join ticketing_cinema on ticketing_house.cinema_id_id = ticketing_cinema.cinema_id) "
                   "join ticketing_movie on ticketing_session.movie_id_id = ticketing_movie.movie_id "
                   "where ticketing_cinema.cinema_id = %s order by start_time;", [cinema_id])
    sessions = cursor.fetchall()
    Sessions = []
    for session in sessions:
        sess = {}
        sess['session_id'] = session[0]
        sess['cinema_name'] = session[1]
        sess['movie_name'] = session[2]
        sess['house_name'] = session[3]
        sess['start_time'] = session[4]
        sess['price'] = session[5]
        Sessions.append(sess)

    # 获取电影院cinema_id的所有的评价
    cursor.execute("select username_id, comment, score from ticketing_cinema_comment where cinema_id_id = %s;",
                   [cinema_id])
    comments = cursor.fetchall()
    Comments = []
    for comment in comments:
        com = {}
        com['username'] = comment[0]
        com['comment'] = comment[1]
        com['score'] = comment[2]
        Comments.append(com)
    context = {'sessions': Sessions, 'comments': Comments, 'cinema': one_cinema, 'movie': False}
    return render(request, 'sessions.html', context)


@login_required(login_url='/users/customer_login/')
def session(request, session_id):
    """显示具体的一个场次，用于在线选座"""
    sess = Session.objects.get(session_id=session_id)
    movie = sess.movie_id
    house = sess.house_id
    cinema = house.cinema_id
    house_all = house.house_type
    orders = Order.objects.filter(session_id=session_id)
    context = {'session': sess, 'movie': movie, 'cinema': cinema, 'house': house, 'house_all': house_all,
               'orders': orders}
    return render(request, 'session.html', context)


@login_required(login_url='/users/customer_login/')
def make_order(request):
    if request.method == "POST":
        seats = request.POST.get('checkID')
        session_id = request.POST.get('session_id')
        price = request.POST.get('price')
        username = request.user.get_username()
        order_time = int(time.time())
        try:
            for seat in seats.split(','):
                if seat == '':
                    break
                seat_row = int(seat.split('-')[-1].split('_')[0])
                seat_column = int(seat.split('-')[-1].split('_')[1])
                session = Session.objects.get(session_id=session_id)
                customer = Customer.objects.get(username=username)
                Order.objects.create(session_id=session, username=customer, time=order_time,
                                     seat_row=seat_row, seat_column=seat_column, status=0, price=price)
            # orders = Order.objects.filter(username=str(username)).order_by('time')
            # context = {'orders': orders}
            # return HttpResponseRedirect(reverse('ticketing:index'))
            return HttpResponse(json.dumps({
                "status": 1,
            }))
        except:
            return HttpResponse(json.dumps({
                "status": 0,
            }))


@login_required(login_url='/users/customer_login/')
def orders(request):
    """显示用户的所有订单"""
    username = request.user.get_username()
    # 获取所有的uesername=用户名的记录，然后将记录按照time逆序排列
    all_orders = Order.objects.filter(username=username)
    times = all_orders.values('time')
    # 获取不同的时间，因为对于不同的用户按照时间分类即可，相同的时间下的肯定是同一单
    distinct_times = set()
    for distinct_time in times:
        distinct_times.add(distinct_time['time'])
    order_infos = []
    distinct_times = [t for t in distinct_times]
    # print(distinct_times)
    for distinct_time in sorted(distinct_times, reverse=True):
        seats = all_orders.filter(time=distinct_time)
        order_info = {}
        session = Session.objects.get(session_id=seats.values('session_id', 'price')[0]['session_id'])
        house = session.house_id
        movie = session.movie_id
        cinema = house.cinema_id
        order_info['order_id'] = distinct_time
        order_info['cinema_name'] = cinema.name
        order_info['cinema_id'] = cinema.cinema_id
        order_info['movie_name'] = movie.name
        order_info['movie_id'] = movie.movie_id
        order_info['house_name'] = house.house_name
        order_info['start_time'] = session.start_time
        order_info['status'] = seats[0].status
        order_info['price'] = len(seats) * seats.values('session_id', 'price')[0]['price']
        order_info['seats'] = []
        for seat in seats.values():
            order_info['seats'].append(str(seat['seat_row']) + '排' + str(seat['seat_column']) + '座')
        order_infos.append(order_info)
    context = {'orders': order_infos}
    return render(request, 'orders.html', context)

@login_required(login_url='/users/customer_login/')
def order(request, order_id):
    """订单支付"""
    username = request.user.get_username()
    Order.objects.filter(username=username, time=order_id).update(status=1)
    return HttpResponseRedirect(reverse('ticketing:orders'))


@login_required(login_url='/users/customer_login/')
def movie_comment(request, movie_id):
    """对于编号为movie_id的电影的评价"""
    movie = Movie.objects.get(movie_id=movie_id)
    user = Customer.objects.get(username=request.user.get_username())
    mcomment = Movie_comment.objects.filter(movie_id=movie_id, username=request.user.get_username())

    if mcomment:
        mcomment = Movie_comment.objects.get(movie_id=movie_id, username=request.user.get_username())
        context = {'movie_comment': mcomment}
        return render(request, 'comment_info.html', context)

    if request.method != 'POST':
        # 未提交数据：创建一个空表单
        form = MovieCommentForm()
    else:
        # POST提交的数据，对数据进行处理
        form = MovieCommentForm(data=request.POST)
        if form.is_valid():
            new_commment = form.save(commit=False)
            new_commment.movie_id = movie
            new_commment.username = user
            new_commment.save()
            return HttpResponseRedirect(reverse('ticketing:orders'))
    context = {'form': form, 'movie_id': movie_id, 'movie_comment': True, 'cinema_comment': False}
    return render(request, 'comment.html', context)


@login_required(login_url='/users/customer_login/')
def cinema_comment(request, cinema_id):
    """对于编号为cinema_id的电影院的评价"""
    cinema = Cinema.objects.get(cinema_id=cinema_id)
    user = Customer.objects.get(username=request.user.get_username())
    ccomment = Cinema_comment.objects.filter(cinema_id=cinema_id, username=request.user.get_username())

    if ccomment:
        ccomment = Cinema_comment.objects.get(cinema_id=cinema_id, username=request.user.get_username())
        context = {'cinema_comment': ccomment}
        return render(request, 'comment_info.html', context)

    if request.method != 'POST':
        # 未提交数据：创建一个空表单
        form = CinemaCommentForm()
    else:
        # POST提交的数据，对数据进行处理
        form = CinemaCommentForm(data=request.POST)
        if form.is_valid():
            new_commment = form.save(commit=False)
            new_commment.cinema_id = cinema
            new_commment.username = user
            new_commment.save()
            return HttpResponseRedirect(reverse('ticketing:orders'))
    context = {'form': form, 'cinema_id': cinema_id, 'movie_comment': False, 'cinema_comment': True}
    return render(request, 'comment.html', context)

