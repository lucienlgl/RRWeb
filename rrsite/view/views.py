from django.shortcuts import render
from django.http import Http404

from rrsite.models import Restaurant


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


# 餐厅页面
def restaurant_view(request, restaurant_id):
    if request.method == 'GET' or request.method == 'HEAD':
        query_set = Restaurant.objects.filter(id=restaurant_id)
        if not query_set:
            return Http404('')
        return render(request, 'rrsite/restaurant.html', context=dict(restaurant_id=restaurant_id))


# 个人主页
def user_view(request):
    if request.method == 'GET' or request.method == 'HEAD':
        return render(request, 'rrsite/user_info.html')
