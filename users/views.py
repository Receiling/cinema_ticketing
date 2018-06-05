from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .forms import CustomerRegisterForm, EmployeeRegisterForm, CustomerLoginForm, EmployeeLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from ticketing.models import Employee, Customer


def logout_view(request):
    """注销用户"""
    # 会清空所有的session，因此不用再另外del request.session['is_customer']
    logout(request)
    return HttpResponseRedirect(reverse('ticketing:index'))


def customer_login(request):
    """顾客登录"""
    if request.method != 'POST':
        # 显示空的登录表单
        form = CustomerLoginForm()
    else:
        # 处理填好的表单
        username = request.POST['username']
        password = request.POST['password']
        customer = Customer.objects.filter(username=username, password=password)
        user = authenticate(username=username, password=password)
        if customer and user is not None and user.is_active:
            login(request, user)
            request.session['customer'] = True
            return HttpResponseRedirect(reverse('ticketing:index'))
        else:
            form = CustomerLoginForm()
            context = {'form': form, 'customer_login': True, 'login_wrong': True}
            return render(request, 'login.html', context)
    context = {'form': form, 'customer_login': True}
    return render(request, 'login.html', context)


def employee_login(request):
    """职工登录"""
    if request.method != 'POST':
        # 显示空的登录表单
        form = EmployeeLoginForm()
    else:
        # 处理填好的表单
        username = request.POST['username']
        password = request.POST['password']
        employee = Employee.objects.filter(username=username, password=password)
        user = authenticate(username=username, password=password)
        if employee and user is not None and user.is_active:
            login(request, user)
            request.session['employee'] = True
            return HttpResponseRedirect(reverse('cinema_backend:index'))
        else:
            form = EmployeeLoginForm()
            context = {'form': form, "employee_login": True, 'login_wrong': True}
            return render(request, 'login.html', context)
    context = {'form': form, "employee_login": True}
    return render(request, 'login.html', context)


def customer_register(request):
    """注册新顾客"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = CustomerRegisterForm()
    else:
        # 处理填好的表单
        form = CustomerRegisterForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            # 让用户自动登录，再重定向到主页
            User = get_user_model()
            User.objects.create_user(username=username, password=password)
            authenticated_user = authenticate(username=username, password=password)
            login(request, authenticated_user)
            form.save()
            request.session['customer'] = True
            return HttpResponseRedirect(reverse('ticketing:index'))
        else:
            form = CustomerRegisterForm()
            context = {'form': form, 'form_invalid': True, 'customer_register': True}
            return render(request, 'register.html', context)
    context = {'form': form, 'customer_register': True}
    return render(request, 'register.html', context)


def employee_register(request):
    """注册新职工"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = EmployeeRegisterForm()
    else:
        # 处理填好的表单
        form = EmployeeRegisterForm(data=request.POST)
        print(form)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            # 让用户自动登录，再重定向到主页
            User = get_user_model()
            User.objects.create_user(username=username, password=password)
            authenticated_user = authenticate(username=username, password=password)
            login(request, authenticated_user)
            form.save()
            request.session['employee'] = True
            return HttpResponseRedirect(reverse('cinema_backend:index'))
        else:
            form = EmployeeRegisterForm()
            context = {'form': form, 'employee_register': True, 'form_invalid': True}
            return render(request, 'register.html', context)
    context = {'form': form, 'employee_register': True}
    return render(request, 'register.html', context)


@login_required(login_url='/users/customer_login/')
def user_info(request):
    username = request.user.get_username()
    user = Customer.objects.filter(username=username)

    if user:
        user = Customer.objects.get(username=username)
        if request.method != 'POST':
            # 初次请求，使用当前条目填充表单
            form = CustomerRegisterForm(instance=user)
        else:
            # POST提交的数据，对数据进行处理
            form = CustomerRegisterForm(instance=user, data=request.POST)
            # print(username, request.POST['username'])
            if username != request.POST['username']:
                form = CustomerRegisterForm(instance=user)
                context = {'form': form, 'customer': True, 'invalid_modify': True}
                return render(request, 'customer_info.html', context)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('users:user_info'))
        context = {'form': form, 'customer': True}
        return render(request, 'customer_info.html', context)
    else:
        user = Employee.objects.get(username=username)
        if request.method != 'POST':
            # 初次请求，使用当前条目填充表单
            form = EmployeeRegisterForm(instance=user)
        else:
            # POST提交的数据，对数据进行处理
            form = EmployeeRegisterForm(instance=user, data=request.POST)
            if username != request.POST['username']:
                form = EmployeeRegisterForm(instance=user)
                context = {'form': form, 'employee': True, 'invalid_modify': True}
                return render(request, 'employee_info.html', context)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('users:user_info'))
        context = {'form': form, 'employee': True}
        return render(request, 'employee_info.html', context)
