"""定义cinema_backend的URL模式"""
from django.conf.urls import url
from . import views

app_name = 'cinema_backend'

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),

    # 影院信息页面
    url(r'^cinema_info/$', views.cinema_info, name='cinema_info'),

    # 场次安排页面
    url(r'^sessions/$', views.sessions, name='sessions'),
    url(r'^arrange/$', views.arrange, name='arrange'),

    # 用户评论页面
    url(r'^comments/$', views.comments, name='comments'),
]