from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection

from ticketing.models import Employee, Cinema, House, Cinema_comment, Session, Movie
from .forms import CinemaInfoForm, SessionFrom
# Create your views here.


@login_required()
def index(request):
    """影院管理系统主页"""
    employee = Employee.objects.get(username=request.user.get_username())
    cinema = employee.cinema_id
    context = {'cinema': cinema}
    return render(request, 'cinema_index.html', context)


@login_required(login_url='/users/employee_login/')
def cinema_info(request):
    """影院信息页面（可以用于更新影院的信息）"""
    employee = Employee.objects.get(username=request.user.get_username())
    cinema = employee.cinema_id
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = CinemaInfoForm(instance=cinema)
    else:
        # POST提交的数据，对数据进行处理
        form = CinemaInfoForm(instance=cinema, data=request.POST)
        # print(username, request.POST['username'])
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cinema_backend:cinema_info'))
    context = {'form': form}
    return render(request, 'cinema_info.html', context)


@login_required(login_url='/users/employee_login/')
def sessions(request):
    """展示影院所有的场次"""
    employee = Employee.objects.get(username=request.user.get_username())
    cinema = employee.cinema_id
    sessions = Session.objects.filter(house_id__cinema_id=cinema.cinema_id)
    Sessions = []
    for session in sessions:
        item = {}
        item['movie_name'] = session.movie_id.name
        item['start_time'] = session.start_time
        item['house_name'] = session.house_id.house_name
        item['price'] = session.price
        Sessions.append(item)
    context = {'sessions': Sessions}
    return render(request, 'cinema_sessions.html', context)


@login_required(login_url='/users/employee_login/')
def arrange(request):
    """场次安排"""
    employee = Employee.objects.get(username=request.user.get_username())
    cinema = employee.cinema_id
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = SessionFrom()
        # 对于外键数据的过滤，通过filter来筛选符合要求的House,而不是在前端页面上显示出所有的house
        form.fields['house_id'].queryset = House.objects.filter(cinema_id=cinema.cinema_id)
    else:
        # POST提交的数据，对数据进行处理
        form = SessionFrom(data=request.POST)
        # print(username, request.POST['username'])
        if form.is_valid():
            new_session = form.save(commit=False)
            new_session.cinema_id = cinema
            print(request.POST.get('date'), request.POST.get('time'))
            new_session.start_time = request.POST['date'] + " " + request.POST['time']
            new_session.save()
            return HttpResponseRedirect(reverse('cinema_backend:sessions'))
    context = {'form': form}
    return render(request, 'add_session.html', context)


@login_required(login_url='/users/employee_login/')
def comments(request):
    """用户评论"""
    employee = Employee.object
    s.get(username=request.user.get_username())
    cinema = employee.cinema_id
    comments = Cinema_comment.objects.filter(cinema_id=cinema.cinema_id)
    context = {'comments': comments}
    return render(request, "cinema_comments.html", context)

