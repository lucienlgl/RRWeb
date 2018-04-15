from django.shortcuts import render, redirect
from django.http import HttpResponse

from rrsite.util.string import username_type
from RRWeb.settings import EMAIL_LOGIN_METHOD, PHONE_LOGIN_METHOD
from rrsite.models import *


# Create your views here.
def index(request):
    return render(request, "rrsite/index.html")


def login(request):
    # 如果是GET或HEAD请求，返回渲染登录页面
    if request.method == 'GET' or request.method == "HEAD":
        return render(request, 'rrsite/login.html')
    # 如果是POST请求，处理表单内容
    elif request.method == 'POST':
        # 获取用户名、密码参数
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        login_method = username_type(username)
        # 登录账号/密码错误信息
        error_login_msg = {'msg': 'Email(Phone Number) or Password Incorrect, Please Check Again'}
        # 登录格式错误信息
        error_format_msg = {'msg': 'Email(Phone Number) Format Incorrect, Please Check Again'}
        # 根据不同登录方式进行登录操作
        # 邮箱登录
        if login_method == EMAIL_LOGIN_METHOD:
            user = CustomUser.objects.filter(email__iexact=username, password__exact=password)
            if user:
                # 将用户名和登录方式存入session实现自动登录机制
                request.session['username'] = username
                request.session['login_method'] = login_method
                # 登录成功，跳转到主页
                return redirect('/')
            else:
                # 账号/密码错误重新渲染页面，返回错误信息
                return render(request, 'rrsite/login.html', context=error_login_msg)
        # 手机号登录
        elif login_method == PHONE_LOGIN_METHOD:
            user = CustomUser.objects.filter(phone__exact=username, password__exact=password)
            if user:
                # 将用户名和登录方式存入session实现自动登录机制
                request.session['username'] = username
                request.session['login_method'] = login_method
                # 登录成功，跳转到主页
                return redirect('/')
            else:
                # 账号/密码错误重新渲染页面，返回错误信息
                return render(request, 'rrsite/login.html', context=error_login_msg)
        else:
            # 账号格式错误重新渲染页面，返回错误信息
            return render(request, 'rrsite/login.html', context=error_format_msg)


def register_view(request):
    return render(request, 'rrsite/register.html')
