from RRWeb.settings import PHONE_LOGIN_METHOD, EMAIL_LOGIN_METHOD
from rrsite.models import CustomUser


def get_login_user(username, login_method):
    try:
        user = None
        if login_method == PHONE_LOGIN_METHOD:
            user = CustomUser.objects.get(phone=username)
        elif login_method == EMAIL_LOGIN_METHOD:
            user = CustomUser.objects.get(email__iexact=username)
        return user
    except CustomUser.DoesNotExist:
        return None


def del_session(request):
    try:
        # 删除session数据
        del request.session['username']
        del request.session['login_method']
        del request.session['login_from']
    except KeyError:
        pass
