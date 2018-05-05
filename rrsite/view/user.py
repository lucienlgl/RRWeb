from django.shortcuts import render, redirect
from django.http import JsonResponse

from rrsite.models import CustomUser
from rrsite.util.utils import username_type, valid_email, valid_phone
from rrsite.util.json import CustomResponseJson
from rrsite.auth.email import *
from rrsite.auth.phone import *
from RRWeb.settings import EMAIL_LOGIN_METHOD, PHONE_LOGIN_METHOD, \
    EMAIL_VERIFY_FAIL_CONTENT, EMAIL_VERIFY_FAIL_TITLE, \
    EMAIL_VERIFY_SUCCEED_CONTENT, EMAIL_VERIFY_SUCCEED_TITLE, \
    ERROR_LOGIN_MSG, ERROR_LOGIN_EMAIL_VALIDATION, ERROR_LOGIN_FORMAT, \
    ERROR_FORM_FORMAT, ERROR_EMAIL_FORMAT, EMAIL_REGISTER_ALREADY, EMAIL_REGISTER_SUCCESS, ERROR_SEND_EMAIL, \
    ERROR_PHONE_FORMAT, ERROR_PHONE_CODE, PHONE_REGISTER_ALREADY, PHONE_REGISTER_SUCCESS


# 登录
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
        # 根据不同登录方式进行登录操作
        # 邮箱登录
        if login_method == EMAIL_LOGIN_METHOD:
            user_query_set = CustomUser.objects.filter(email__iexact=username, password__exact=password)
            if user_query_set:
                # 如果邮箱未激活，禁止登录
                if user_query_set[0].is_active == 0:
                    return render(request, 'rrsite/login.html', context=ERROR_LOGIN_EMAIL_VALIDATION)
                # 将用户名和登录方式存入session实现自动登录机制
                request.session['username'] = username
                request.session['login_method'] = login_method
                # 登录成功，跳转到主页
                return redirect('/')
            else:
                # 账号/密码错误重新渲染页面，返回错误信息
                return render(request, 'rrsite/login.html', context=ERROR_LOGIN_MSG)
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
                return render(request, 'rrsite/login.html', context=ERROR_LOGIN_MSG)
        else:
            # 账号格式错误重新渲染页面，返回错误信息
            return render(request, 'rrsite/login.html', context=ERROR_LOGIN_FORMAT)


def logout(request):
    # 退出登录，返回主页
    response = render(request, 'rrsite/index.html')
    try:
        # 删除session数据
        del request.session['username']
        del request.session['login_method']
        # 删除cookies
        response.delete_cookie('username')
    except KeyError:
        pass
    return response


# 邮箱注册
def register_email(request):
    # 只处理POST请求，否则跳转到注册页面
    if request.method == 'POST':
        # 获取email、password、confirmPassword字段
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirmPassword', None)
        # 如果字段为空，返回页面和错误表单信息
        if email is None or password != confirm_password:
            return render(request, 'rrsite/register.html', context=ERROR_FORM_FORMAT)
        # 如果email格式正确，添加账号并发送激活账号邮件
        if valid_email(email):
            query_set = CustomUser.objects.filter(email__iexact=email, password=password)
            if query_set:
                # 若用户已注册，返回错误信息
                return render(request, 'rrsite/register.html', context=EMAIL_REGISTER_ALREADY)
            else:
                # 发送激活邮件，成功发送，添加用户到数据库，跳转到登录页面
                if send_register_email(email) == 1:
                    # 添加用户
                    user = CustomUser.objects.create(email=email, password=password)
                    user.save()
                    return render(request, 'rrsite/login.html', context=EMAIL_REGISTER_SUCCESS)
                else:
                    # 发送激活邮件失败，返回错误信息
                    return render(request, 'rrsite/register.html', context=ERROR_SEND_EMAIL)
        else:
            # email格式错误，返回错误信息
            return render(request, 'rrsite/register.html', context=ERROR_EMAIL_FORMAT)
    else:
        # 跳转到注册页面
        return redirect('/register')


# 手机号码注册
def register_phone(request):
    # 只处理POST请求，否则跳转到注册页面
    if request.method == 'POST':
        # 获取phone、password、confirmPassword字段
        phone = request.POST.get('phone', None)
        code = request.POST.get('code', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirmPassword', None)
        # 如果字段为空，返回页面和错误表单信息
        if phone is None or code is None or password != confirm_password:
            return render(request, 'rrsite/register.html', context=ERROR_PHONE_FORMAT)
        # 如果phone格式正确，检查验证码，添加账号
        if valid_phone(phone):
            query_set = CustomUser.objects.filter(phone=phone, password=password)
            if query_set:
                # 若用户已注册，返回错误信息
                return render(request, 'rrsite/register.html', context=PHONE_REGISTER_ALREADY)
            else:
                if check_phone_code(phone, code):
                    # 验证码正确，添加，激活用户
                    user = CustomUser.objects.create(phone=phone, password=password, is_active=1)
                    user.save()
                    return render(request, 'rrsite/login.html', context=PHONE_REGISTER_SUCCESS)
                else:
                    # 验证码错误，返回错误信息
                    return render(request, 'rrsite/register.html', context=ERROR_PHONE_CODE)
        else:
            # 手机号格式错误，返回错误信息
            return render(request, 'rrsite/register.html', context=ERROR_PHONE_FORMAT)
    else:
        # 跳转到注册页面
        return redirect('/register')


def send_forget_mail(request):
    pass


def forget_password(request):
    if request.method == 'GET' or request.method == 'HEAD':
        return render(request, 'rrsite/forgetpassword.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        if email is not None and phone is None:
            user = CustomUser.objects.filter(email__iexact=email)
            if user:
                user = user[0]
                user.password = password
                user.save()
                return render(request, 'rrsite/login.html',
                              context={'msg': 'Password Change Succeed, You Can Login Now'})
            else:
                return render(request, 'rrsite/forgetpassword.html',
                              context={'msg_email': 'Email incorrect!!!'})
        elif email is None and phone is not None:
            user = CustomUser.objects.filter(phone__iexact=phone)
            if user:
                user = user[0]
                user.password = password
                user.save()
                return render(request, 'rrsite/login.html',
                              context={'msg': 'Password Change Succeed, You Can Login Now'})
            else:
                return render(request, 'rrsite/forgetpassword.html',
                              context={'msg_phone': 'Phone Incorrect!!!'})
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


def basic_info(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname', None)
        sex = request.POST.get('sex', None)
        birthday = request.POST.get('birthday', None)
        location = request.POST.get('location', None)
        remark = request.POST.get('remark', None)

        login_method = request.session.get('login_method', None)
        username = request.session.get('username', None)

        user = None
        if login_method is not None:
            if login_method == EMAIL_LOGIN_METHOD:
                user = CustomUser.objects.get(email__iexact=username)
            elif login_method == PHONE_LOGIN_METHOD:
                user = CustomUser.objects.get(phone=username)
            if isinstance(user, CustomUser):
                user.sex = sex
                user.nickname = nickname
                user.location = location
                user.remark = remark
                user.birthday = birthday
                user.save()
                return JsonResponse(CustomResponseJson(msg='保存成功', code=1))
        return JsonResponse(CustomResponseJson(msg='保存失败，请重新登录', code=0))