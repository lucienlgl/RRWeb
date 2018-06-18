from django.shortcuts import render, redirect
from django.http import JsonResponse

from rrsite.models import CustomUser, User, Review, Favor
from rrsite.util.utils import username_type, valid_email, valid_phone
from rrsite.util.json import CustomResponseJson
from rrsite.util.user import get_login_user, del_session
from rrsite.auth.email import *
from rrsite.auth.phone import *
from RRWeb.settings import EMAIL_LOGIN_METHOD, PHONE_LOGIN_METHOD, \
    EMAIL_VERIFY_FAIL_CONTENT, EMAIL_VERIFY_FAIL_TITLE, \
    EMAIL_VERIFY_SUCCEED_CONTENT, EMAIL_VERIFY_SUCCEED_TITLE, \
    ERROR_LOGIN_MSG, ERROR_LOGIN_EMAIL_VALIDATION, ERROR_LOGIN_FORMAT, \
    ERROR_FORM_FORMAT, ERROR_EMAIL_FORMAT, EMAIL_REGISTER_ALREADY, \
    EMAIL_REGISTER_SUCCESS, ERROR_SEND_EMAIL, ERROR_PHONE_FORMAT, \
    ERROR_PHONE_CODE, PHONE_REGISTER_ALREADY, PHONE_REGISTER_SUCCESS, \
    PHONE_CODE_SEND_FAILED, PHONE_VERIFY_MINUTES


# 登录
def login(request):
    # 如果是GET或HEAD请求，返回渲染登录页面
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
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
                return redirect(request.session.get('login_from', '/'))
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
                # return redirect('/')
                return redirect(request.session.get('login_from', '/'))
            else:
                # 账号/密码错误重新渲染页面，返回错误信息
                return render(request, 'rrsite/login.html', context=ERROR_LOGIN_MSG)
        else:
            # 账号格式错误重新渲染页面，返回错误信息
            return render(request, 'rrsite/login.html', context=ERROR_LOGIN_FORMAT)


# 退出登录，返回主页
def logout(request):
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    del_session(request)
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
                if send_email(email) == 1:
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
                code = random_phone_code()
                result, errmsg = send_phone_code(phone=phone, code=code, minute=5)
                if result != 0:
                    return render(request, 'rrsite/login.html', context=PHONE_CODE_SEND_FAILED)
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
    if request.method == 'GET':
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


def email_verify(request, token):
    if request.method != 'GET':
        return redirect('/')

    email = request.GET.get('email', None)
    send_type = request.GET.get('type', None)

    if email is None or email == '':
        return render(request, 'rrsite/emailactivation.html',
                      {'msg_title': EMAIL_VERIFY_FAIL_TITLE, 'msg_content': EMAIL_VERIFY_FAIL_CONTENT})

    if check_email_code(email=email, code=token, send_type=send_type):
        user = CustomUser.objects.get(email=email)
        user.is_active = 1
        user.save()
        return render(request, 'rrsite/emailactivation.html',
                      {'msg_title': EMAIL_VERIFY_SUCCEED_TITLE, 'msg_content': EMAIL_VERIFY_SUCCEED_CONTENT})
    else:
        return render(request, 'rrsite/emailactivation.html',
                      {'msg_title': EMAIL_VERIFY_FAIL_TITLE, 'msg_content': EMAIL_VERIFY_FAIL_CONTENT})


# 获取用户基本信息，修改用户基本信息
def basic_info(request):
    # 接受POST修改用户信息操作
    if request.method == 'POST':
        # 获取基本信息，昵称，性别，位置，留言
        nickname = request.POST.get('nickname', None)
        sex = request.POST.get('sex', None)
        location = request.POST.get('location', None)
        remark = request.POST.get('remark', None)

        # 获取session中信息
        username = request.session.get('username', None)
        login_method = request.session.get('login_method', None)

        # 获取已登录用户对象
        user = get_login_user(username, login_method)
        # 如果user为None，返回错误信息
        if not isinstance(user, CustomUser):
            return JsonResponse(CustomResponseJson(msg='请重新登录', code=0))

        try:
            # 修改个人基本信息
            user.sex = sex
            user.nickname = nickname
            user.location = location
            user.remark = remark
            user.save()
            return JsonResponse(CustomResponseJson(msg='保存成功', code=1))
        except Exception as e:
            print(e)
            return JsonResponse(CustomResponseJson(msg='保存失败', code=0))
    elif request.method == 'GET':
        user_id = request.GET.get('id', None)
        if user_id is None:
            login_method = request.session.get('login_method', None)
            username = request.session.get('username', None)
            try:
                user = get_login_user(username, login_method)
                if user is not None:
                    data = dict(name=user.name, sex=user.sex, location=user.location, remark=user.remark,
                                email=user.email, phone=user.phone)
                    return JsonResponse(CustomResponseJson(msg='获取用户信息成功', code=1, data=data))
                else:
                    return JsonResponse(CustomResponseJson(msg='请重新登录', code=0))
            except CustomUser.DoesNotExist:
                return JsonResponse(CustomResponseJson(msg='请重新登录', code=0))
        user = list(User.objects.filter(id=user_id).values())
        if not user:
            user = list(CustomUser.objects.filter(id=user_id).values())
        if user:
            return JsonResponse(CustomResponseJson(msg='获取用户信息成功', code=1, data=user[0]))
        else:
            return JsonResponse(CustomResponseJson(msg='用户ID错误', code=0))
    else:
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))


def user_info(request):
    if request.method != 'GET':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))
    user_id = request.GET.get('id', None)
    login_method = request.session.get('login_method', None)
    username = request.session.get('username', None)
    user = get_login_user(username, login_method)
    data = dict(is_self=False)
    if user and user.id == user_id:
        data['is_self'] = True
    if str(user_id).isdigit():
        info = list(CustomUser.objects.filter(id=user_id).values())
        data['reviews'] = list(Review.objects.filter(custom_user_id=user_id).values())
        data['collections'] = list(Favor.objects.filter(custom_user_id=user_id).values())
    else:
        info = list(User.objects.filter(id=user_id).values())
        data['reviews'] = list(Review.objects.filter(user_id=user_id).values())
        data['collections'] = list()
    if info:
        data['info'] = info[0]
    return JsonResponse(CustomResponseJson(msg='获取成功', code=1, data=data))


# 发送验证码
def phone_code(request):
    # 只处理POST请求，否则返回错误信息
    if request.method != 'POST':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))

    # 获取电话号参数
    phone = request.POST.get('phone', None)

    # 如果手机号为空，返回错误信息
    if phone is None or str(phone) == '':
        return JsonResponse(CustomResponseJson(msg='手机号不能为空', code=0))

    # 生成随机验证码
    code = random_phone_code()

    # 发送验证码，接受发送结果信息
    # 设置发送手机号，发送随机验证码，验证码过期时间
    result, errmsg = send_phone_code(phone=phone, code=code, minute=PHONE_VERIFY_MINUTES)

    # 返回发送信息是否成功
    if result == 0:
        return JsonResponse(CustomResponseJson(msg='发送验证码成功', code=1))
    else:
        return JsonResponse(CustomResponseJson(msg='发送验证码失败' + errmsg, code=0))


# 更改手机号
def change_phone(request):
    # 只处理POST请求，否则返回错误信息
    if request.method != 'POST':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))

    # 获取电话号参数
    phone = request.POST.get('phone', None)
    # 获取验证码参数
    code = request.POST.get('code', None)

    # 如果不是正确手机号格式，返回错误信息
    if not valid_phone(phone):
        return JsonResponse(CustomResponseJson(msg='手机号格式错误', code=0))

    # 检查验证码是否正确，是否过期
    result, err_msg = check_phone_code(phone=phone, code=code)

    # 如果检查结果为False，返回错误信息
    if not result:
        return JsonResponse(CustomResponseJson(msg=err_msg, code=0))

    # 获取已登录用户对象
    user = get_login_user(request.session.get('username', None), request.session.get('login_method', None))

    # 如果user为None，返回错误信息
    if not isinstance(user, CustomUser):
        return JsonResponse(CustomResponseJson(msg='请重新登录', code=0))
    try:
        # 保存用户新手机号
        user.phone = phone
        user.save()
        # 删除session值，强制用户下线
        del_session(request)
        # 返回正确信息
        return JsonResponse(CustomResponseJson(msg='修改手机号成功,请重新登录', code=1))
    except Exception as e:
        print(e)
        return JsonResponse(CustomResponseJson(msg='修改手机号失败', code=0))


# 更改邮箱
def change_email(request):
    # 只处理POST请求，否则返回错误信息
    if request.method != 'POST':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))

    # 获取邮箱参数
    email = request.POST.get('email', None)

    # 如果不是正确邮箱格式，返回错误信息
    if not valid_email(email):
        return JsonResponse(CustomResponseJson(msg='邮箱格式错误', code=0))

    # 如果发送激活邮件错误，返回错误信息
    if send_email(email=email, send_type='change') != 1:
        return JsonResponse(CustomResponseJson(msg='发送邮件失败', code=0))

    # 获取已登录用户对象
    user = get_login_user(request.session.get('username', None), request.session.get('login_method', None))

    # 如果user为None，返回错误信息
    if not isinstance(user, CustomUser):
        return JsonResponse(CustomResponseJson(msg='请重新登录', code=0))
    try:
        # 保存用户新邮箱号
        user.email = email
        user.is_active = 0
        user.save()
        # 删除session值，强制用户下线
        del_session(request)
        # 返回正确信息
        return JsonResponse(CustomResponseJson(msg='更改邮箱成功,请先激活新邮箱后登录', code=1))
    except Exception as e:
        print(e)
        return JsonResponse(CustomResponseJson(msg='修改邮箱失败', code=0))


def change_password(request):
    # 只处理POST请求，否则返回错误信息
    if request.method != 'POST':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))

    # 获取旧密码，新密码参数
    cur_password = request.POST.get('password', None)
    new_password = request.POST.get('new_password', None)
    confirm = request.POST.get('confirm_password', None)

    # 如果密码为空，返回错误信息
    if cur_password is None or '' == cur_password or new_password is None \
            or '' == new_password or confirm is None or '' == confirm:
        return JsonResponse(CustomResponseJson(msg='密码不能为空', code=0))

    # 如果两次新密码不一致，返回错误信息
    if new_password != confirm:
        return JsonResponse(CustomResponseJson(msg='两次输入密码不一致', code=0))

    # 获取已登录用户对象
    user = get_login_user(request.session.get('username', None), request.session.get('login_method', None))

    # 如果user为None，返回错误信息
    if not isinstance(user, CustomUser):
        return JsonResponse(CustomResponseJson(msg='请重新登录', code=0))

    # 如果旧密码输入错误，返回错误信息
    if user.password != cur_password:
        return JsonResponse(CustomResponseJson(msg='旧密码错误', code=0))

    try:
        # 保存用户新密码
        user.password = new_password
        user.save()
        # 删除session值，强制用户下线
        del_session(request)
        return JsonResponse(CustomResponseJson(msg='密码修改成功', code=1))
    except Exception as e:
        print(e)
        return JsonResponse(CustomResponseJson(msg='密码修改失败', code=0))


def user_page(request):
    return render(request, 'rrsite/user_page.html')
