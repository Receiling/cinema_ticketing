"""定义ticketing的URL模式"""
from django.conf.urls import url
from . import views

app_name = 'ticketing'

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),

    # 电影页面
    url(r'^movies/$', views.movies, name='movies'),
    url(r'^movie/(?P<movie_id>\d+)/$', views.movie, name='movie'),

    # 影院页面
    url(r'^cinemas/$', views.cinemas, name='cinemas'),
    url(r'cinema/(?P<cinema_id>\d+)/$', views.cinema, name='cinema'),

    # 选座页面
    url(r'^session/(?P<session_id>\d+)/$', views.session, name='session'),

    # 用户订单页面
    url(r'^make_order/$', views.make_order, name='make_order'),
    url(r'^orders/$', views.orders, name='orders'),

    # 用户评价页面
    url(r'^movie_comment/(?P<movie_id>\d+)/$', views.movie_comment, name='movie_comment'),
    url(r'^cinema_comment/(?P<cinema_id>\d+)/$', views.cinema_comment, name='cinema_comment'),
]