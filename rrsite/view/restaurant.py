import uuid

import os
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage

from rrsite.models import Photo, Restaurant, Category, Hour, Tip, Review, \
    Attribute, User, Friend, CustomUser, CustomFriend, Favor
from rrsite.util.json import CustomResponseJson
from rrsite.util.user import get_login_user
from RRWeb.settings import PHOTO_STATIC_URL_FORMAT

from RRWeb.settings import BASE_DIR
import json

from uuid import uuid4


def basic_info(request):
    if request.method != 'GET':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))
    restaurant_id = request.GET.get('id', None)
    if restaurant_id is None:
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID不能为空', code=0))
    restaurant_list = list(Restaurant.objects.filter(id=restaurant_id).values())
    if not restaurant_list:
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID错误', code=0))
    info = restaurant_list[0]
    categories_list = list(Category.objects.filter(restaurant_id=restaurant_id).values('category'))
    categories_list = [category_dict['category'] for category_dict in categories_list]
    info['categories'] = categories_list
    hours_list = list(Hour.objects.filter(restaurant_id=restaurant_id).values('day', 'hours'))
    info['hours'] = dict()
    for hours in hours_list:
        info['hours'][hours['day']] = hours['hours']
    return JsonResponse(CustomResponseJson(msg='查询餐厅基本信息成功', code=1, data=info))


def special_info(request):
    if request.method != 'GET':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))
    restaurant_id = request.GET.get('id', None)
    if restaurant_id is None:
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID不能为空', code=0))
    attribute_list = list(Attribute.objects.filter(restaurant_id=restaurant_id).values('name', 'value'))
    if not attribute_list:
        return JsonResponse(CustomResponseJson(msg='餐厅不存在或特殊信息为空', code=0))
    data = dict()
    for attribute_dict in attribute_list:
        name = attribute_dict.get('name', '')
        value = attribute_dict.get('value', '')
        if '_' not in name:
            data[name] = value
        else:
            main_sub = str(name).split('_')
            if main_sub[0] not in data:
                data[main_sub[0]] = dict()
            data[main_sub[0]][main_sub[1]] = value
    return JsonResponse(CustomResponseJson(msg='查询餐厅特殊信息成功', code=1, data=data))


def photo_info(request):
    if request.method != 'GET':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))

    restaurant_id = request.GET.get('id', None)
    cur_page_num = request.GET.get('page', 1)

    if restaurant_id is None:
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID不能为空', code=0))

    photos = Photo.objects.filter(restaurant_id=restaurant_id).values('id', 'caption', 'label')

    pages = Paginator(photos, 9)

    if pages.count == 0:
        return JsonResponse(CustomResponseJson(msg='无图片信息', code=0))

    try:
        photos = pages.page(cur_page_num)
        data = dict(photo_num=pages.count, page_num=pages.num_pages, has_pre=photos.has_previous(),
                    has_next=photos.has_next(), photos_this_page=len(photos), photos=[])
        for info in photos:
            photo_dict = dict(url=PHOTO_STATIC_URL_FORMAT.format(info['id']), caption=info['caption'],
                              label=info['label'])
            data['photos'].append(photo_dict)
        return JsonResponse(CustomResponseJson(msg='获取第{0}页餐厅图片成功'.format(cur_page_num), code=1, data=data))
    except EmptyPage as e:
        return JsonResponse(CustomResponseJson(msg='页码错误,{0}'.format(e), code=0))


def tips_info(request):
    if request.method != 'GET':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))
    restaurant_id = request.GET.get('id', None)
    if restaurant_id is None:
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID不能为空', code=0))
    count = Tip.objects.filter(restaurant_id=restaurant_id).count()
    if count == 0:
        return JsonResponse(CustomResponseJson(msg='餐厅简评为空', code=0))
    data = dict(tips_num=count, tips=list(
        Tip.objects.filter(restaurant_id=restaurant_id).order_by('?')[:5].values('id', 'user_id', 'custom_user',
                                                                                 'text', 'date', 'likes')))
    return JsonResponse(CustomResponseJson(msg='查询餐厅简评成功', code=1, data=data))


def review_info(request):
    if request.method == 'GET':
        restaurant_id = request.GET.get('id', None)
        current_page = request.GET.get('page', 1)
        order = request.GET.get('order', '-date')
        if restaurant_id is None:
            return JsonResponse(CustomResponseJson(msg='传入餐厅ID不能为空', code=0))
        reviews = Review.objects.filter(restaurant_id=restaurant_id).order_by(order).values()
        pages = Paginator(reviews, 10)
        try:
            reviews = pages.page(current_page)
            data = dict(reviews_sum=pages.count, page_num=pages.num_pages, has_pre=reviews.has_previous(),
                        has_next=reviews.has_next(), reviews_this_page=len(reviews), reviews=list(reviews))
            for review in data.get('reviews', []):
                user_id = review.get('user_id', None)
                if user_id is None:
                    user_id = review.get('custom_user_id', None)
                    user = CustomUser.objects.get(id=user_id)
                    friend_count = CustomFriend.objects.filter(custom_user_id=user_id).count()
                else:
                    user = User.objects.get(id=user_id)
                    friend_count = Friend.objects.filter(user_id=user_id).count()
                review['user'] = dict(name=user.name, review_count=user.review_count, friend_count=friend_count)
            return JsonResponse(CustomResponseJson(
                msg='获取餐厅第{0}页评价成功'.format(current_page), code=1, data=data))
        except EmptyPage as e:
            return JsonResponse(CustomResponseJson(msg='页码错误,{0}'.format(e), code=0))
    elif request.method == 'POST':

        restaurant_id = request.POST.get('id', None)
        stars = request.POST.get('stars', None)
        text = request.POST.get('text', None)

        if restaurant_id is None or '' == restaurant_id:
            return JsonResponse(CustomResponseJson(msg='传入餐厅ID不能为空', code=0))

        if text is None or '' == text:
            return JsonResponse(CustomResponseJson(msg='评论内容不能为空', code=0))

        try:
            stars = int(stars)
            if not 0 < stars < 6:
                return JsonResponse(CustomResponseJson(msg='打分只能为1-5', code=0))
        except ValueError:
            return JsonResponse(CustomResponseJson(msg='打分只能为数字', code=0))

        # 获取已登录用户对象
        user = get_login_user(request.session.get('username', None), request.session.get('login_method', None))

        # 如果user为None，返回错误信息
        if not isinstance(user, CustomUser):
            return JsonResponse(CustomResponseJson(msg='请登录', code=0))

        try:
            review = Review.objects.create(id=str(uuid4()).replace('-', ''), restaurant_id=restaurant_id,
                                           custom_user_id=user.id, user_id=None)
            review.text = text
            review.stars = stars
            review.save()
            user.review_count = user.review_count + 1
            user.save()
            return JsonResponse(CustomResponseJson(msg='评论成功', code=1))
        except Exception as e:
            print(e)
            return JsonResponse(CustomResponseJson(msg='评论失败', code=0))
    else:
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))


def recommend(request):
    if request.method != 'GET':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))

    category = request.GET.get('category', None)
    if category is None:
        return JsonResponse(CustomResponseJson('传入参数错误', 0))
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
    return JsonResponse(CustomResponseJson('请求成功', 1, restaurants_values_list))


def add_favor(request):
    if request.method != 'POST':
        return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0))
    restaurant_id = request.POST.get('id', None)
    if not restaurant_id:
        return JsonResponse(CustomResponseJson(msg='传入参数错误', code=0))
    user = get_login_user(request.session.get('username', None), request.session.get('login_method', None))
    if not user:
        return JsonResponse(CustomResponseJson(msg='请先登录', code=0))
    favor, _ = Favor.objects.get_or_create(custom_user_id=user.id, restaurant_id=restaurant_id)
    favor.save()
    return JsonResponse(CustomResponseJson(msg='收藏成功', code=1))


def uploadfile(request):
    if request.method == "POST":
        restaurant_id = request.POST.get('id', None)
        if not restaurant_id:
            resp = {'code': 0, 'msg': '传入参数错误'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="text/html")
        user = get_login_user(request.session.get('username', None), request.session.get('login_method', None))
        if not user:
            resp = {'code': 0, 'msg': '请先登录'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="text/html")
        im = str(request.FILES['file'].name).split('.')
        name = str(uuid.uuid1()) + '.' + im[len(im)-1]
        if handle_upload_file(request.FILES['file'], name):
            photo = Photo.objects.create(custom_user_id=user.id, id=name.split('.')[0], restaurant_id=restaurant_id)
            photo.save()
            # 返回JSON数据
            resp = {'code': 1, 'msg': '上传成功'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="text/html")
        else:
            resp = {'code': 0, 'msg': '上传失败'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="text/html")


def handle_upload_file(file, filename):
    path = os.path.join(BASE_DIR, 'rrsite/static/rrsite/upload_photo/')  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb+')as destination:
        for chunk in file.chunks():
           destination.write(chunk)
    return True
