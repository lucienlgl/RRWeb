from django.shortcuts import render


# 主页
def index(request):
    res = render(request, 'rrsite/index.html')
    username = request.session.get('username', None)
    if username is not None:
        res.set_cookie('username', username)
    else:
        res.delete_cookie('username')
    return res


# 注册页面
def register_view(request):
    if request.method == 'GET' or request.method == 'HEAD':
        return render(request, 'rrsite/register.html')
