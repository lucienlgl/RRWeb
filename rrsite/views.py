from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime

from rrsite.models import CustomUser, Restaurant, Photo, Review, CustomResponseMessage
from rrsite.util.string import username_type, valid_email, valid_phone
from RRWeb.settings import EMAIL_LOGIN_METHOD, PHONE_LOGIN_METHOD, \
    PHOTO_STATIC_URL_FORMAT, EMAIL_VERIFY_FAIL_TITLE, EMAIL_VERIFY_FAIL_CONTENT, \
    EMAIL_VERIFY_SUCCEED_TITLE, EMAIL_VERIFY_SUCCEED_CONTENT
from rrsite.auth.email import *
from rrsite.auth.phone import *


# Create your views here.
def index(request):

    res = render(request, 'rrsite/index.html')
    username = request.session.get('username', None)
    if username is not None:
        res.set_cookie('username', username)
    else:
        res.delete_cookie('username')
    return res


def login(request):
    # 如果是GET或HEAD请求，返回渲染登录页面
    if request.method == 'GET' or request.method == "HEAD":
        return render(request, 'rrsite/login.html')
    # 如果是POST请求，处理表单内容
    elif request.method == 'POST':
        # 获取用户名、密码参数
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        login_method = username_type(username)
        # 登录账号/密码错误信息
        error_login_msg = {'msg': 'Email(Phone Number) or Password Incorrect, Please Check Again'}
        error_login_msg_email_validation = {'msg': 'Please Check Your Email and Verify the Email Address First'}
        # 登录格式错误信息
        error_format_msg = {'msg': 'Email(Phone Number) Format Incorrect, Please Check Again'}
        # 根据不同登录方式进行登录操作
        # 邮箱登录
        if login_method == EMAIL_LOGIN_METHOD:
            user_query_set = CustomUser.objects.filter(email__iexact=username, password__exact=password)
            if user_query_set:
                if user_query_set[0].is_active == 0:
                    return render(request, 'rrsite/login.html', context=error_login_msg_email_validation)
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
            user_query_set = CustomUser.objects.filter(phone__exact=username, password__exact=password)
            if user_query_set:
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
    if request.method == 'GET' or request.method == 'HEAD':
        return render(request, 'rrsite/register.html')


def register_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirmPassword', None)
        error_email_format = {'error_email_msg': 'Your Email \'s Format is Incorrect'}
        if email is None or password is None or confirm_password is None:
            return render(request, 'rrsite/register.html', context=error_email_format)
        error_send_email = {'msg': 'Sending Authentication Email Failed. Please Check Your Email'}
        register_success_msg = {'msg': 'Email Register Success! Please Check Your Email '
                                       'and Activate the Account ASAP! You Can Login Now'}
        if valid_email(email):
            if send_register_email(email) == 1:
                user = CustomUser.objects.create(email=email, password=password, is_superuser=0, is_staff=0,
                                                 is_active=1, last_login=datetime.now()
                                                 , date_joined=datetime.now())
                user.save()
                return render(request, 'rrsite/login.html', context=register_success_msg)
            else:
                return render(request, 'rrsite/register.html', context=error_send_email)
        else:
            return render(request, 'rrsite/register.html', context=error_email_format)
    else:
        return redirect('/register')


def register_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', None)
        code = request.POST.get('code', None)
        password = request.POST.get('password', None)
        error_phone_format = {'error_phone_msg': 'Your Phone \'s Format is Incorrect'}
        error_send_phone = {'error_phone_msg': 'Your Phone \'s Format is Incorrect'}
        register_success_msg = {'msg': 'Phone Register Success! You Can Login Now!'}
        if valid_phone(phone):
            if check_phone_code(phone, code):
                user = CustomUser.objects.create(phone=phone, password=password, is_superuser=0, is_staff=0, is_active=1
                                                 , last_login=datetime.now(), date_joined=datetime.now())
                user.save()
                return render(request, 'rrsite/login.html', context=register_success_msg)
            else:
                return render(request, 'rrsite/register.html', context=error_send_phone)
        else:
            return render(request, 'rrsite/register.html', context=error_phone_format)
    else:
        return redirect('/register')


def recommend_restaurant(request):
    if request.method == 'GET' or request.method == 'HEAD':
        category = request.GET.get('category', None)
        if category is not None and category != '':
            category = str(category).replace('_', ' ')
            restaurants_values_list = list(Restaurant.objects
                                           .filter(category__category__iexact=category, review_count__gte=400)
                                           .order_by('?')[:6].values())
            for restaurants_dict in restaurants_values_list:
                photo_query_set = Photo.objects.filter(restaurant_id=restaurants_dict.get('id', None))[:1]
                photo_id = ''
                if photo_query_set:
                    photo_id = photo_query_set[0].id
                if photo_id != '':
                    restaurants_dict['photo_url'] = PHOTO_STATIC_URL_FORMAT.format(photo_id)
                else:
                    restaurants_dict['photo_url'] = ''
            return JsonResponse(CustomResponseMessage('请求成功', 1, restaurants_values_list).__str__())
        else:
            return JsonResponse(CustomResponseMessage('传入参数错误', 0).__str__())
    else:
        return JsonResponse(CustomResponseMessage('传入参数错误', 0).__str__())


def hot_review(request):
    if request.method == 'GET' or request.method == 'HEAD':
        restaurants_values_list = list(Restaurant.objects.filter(review_count__gte=500).order_by('?')[:5].values())
        review_list = []
        for restaurant_dict in restaurants_values_list:
            review_dict = Review.objects.filter(restaurant_id=restaurant_dict.get('id', None),
                                                )[:1]. \
                                                values('id', 'restaurant_id', 'restaurant__name', 'user_id',
                                                       'user__name', 'stars', 'date', 'text')[0]
            review_list.append(review_dict)
            photo_query_set = Photo.objects.filter(restaurant_id=restaurant_dict.get('id', None))[:1]
            photo_id = ''
            if photo_query_set:
                photo_id = photo_query_set[0].id
            if photo_id != '':
                review_dict['photo_url'] = PHOTO_STATIC_URL_FORMAT.format(photo_id)
            else:
                review_dict['photo_url'] = ''
        return JsonResponse(CustomResponseMessage('请求成功', 1, review_list).__str__())
    else:
        return JsonResponse(CustomResponseMessage('请求方法错误', 0).__str__())


def forget_password(request):
    if request.method == 'GET' or request.method == 'HEAD':
        return render(request, 'rrsite/forgetpassword.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        if email is not None and phone is None:
            pass
        elif email is None and phone is not None:
            pass
        else:
            return render(request, 'rrsite/forgetpassword.html', context={})
    else:
        return redirect('/forgot_password')


def email_validation(request, token):
    if request.method == 'GET' or request.method == 'HEAD':
        email = request.GET.get('email', None)
        if email is not None and email != '':
            record = EmailVerifyRecord.objects.filter(email__iexact=email, code__exact=token, send_type__exact='register')
            if record:
                user = CustomUser.objects.get(email=email)
                user.is_active = 1
                user.save()
                return render(request, 'rrsite/emailactivation.html'
                              , {'msg_title': EMAIL_VERIFY_SUCCEED_TITLE, 'msg_content': EMAIL_VERIFY_SUCCEED_CONTENT})
            else:
                return render(request, 'rrsite/emailactivation.html'
                              , {'msg_title': EMAIL_VERIFY_FAIL_TITLE, 'msg_content': EMAIL_VERIFY_FAIL_CONTENT})
        else:
            return render(request, 'rrsite/emailactivation.html'
                          , {'msg_title': EMAIL_VERIFY_FAIL_TITLE, 'msg_content': EMAIL_VERIFY_FAIL_CONTENT})
    else:
        return redirect('/')
