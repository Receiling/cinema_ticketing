"""定义users的URL模式"""
from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    # 登录页面
    url(r'^customer_login/$', views.customer_login, name='customer_login'),
    url(r'^employee_login/$', views.employee_login, name='employee_login'),

    # 登出页面
    url(r'^logout/$', views.logout_view, name='logout'),

    # 注册页面
    url(r'^customer_register/$', views.customer_register, name='customer_register'),
    url(r'^employee_register/$', views.employee_register, name='employee_register'),

    # 用户信息页面
    url(r'^user_info/$', views.user_info, name='user_info'),
]