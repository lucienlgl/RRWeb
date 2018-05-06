from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage

from rrsite.models import Photo, Restaurant, Category, Hours, Tip, Review
from rrsite.util.json import CustomResponseJson
from RRWeb.settings import PHOTO_STATIC_URL_FORMAT


def basic_info(request):
    if request.method == 'GET':
        restaurant_id = request.GET.get('id', None)
        if restaurant_id is not None:
            restaurant_list = list(Restaurant.objects.filter(id=restaurant_id).values())
            if restaurant_list:
                info = restaurant_list[0]
                categories_list = list(Category.objects.filter(restaurant_id=restaurant_id).values('category'))
                categories_list = [category_dict['category'] for category_dict in categories_list]
                info['categories'] = categories_list
                hours_list = list(Hours.objects.filter(restaurant_id=restaurant_id).values('day', 'hours'))
                info['hours'] = hours_list
                return JsonResponse(CustomResponseJson(msg='查询餐厅基本信息成功', code=1, data=info).__str__())
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID错误', code=0).__str__())
    return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0).__str__())


def photo_info(request):
    if request.method == 'GET':
        restaurant_id = request.GET.get('id', None)
        if restaurant_id is not None:
            count = Photo.objects.filter(restaurant_id=restaurant_id).count()
            data = {'photo_num': count, 'photos': []}
            photo_list = list(
                Photo.objects.filter(restaurant_id=restaurant_id).order_by('?')[:9].values('id', 'caption', 'label'))
            for info in photo_list:
                photo_dict = {"url": PHOTO_STATIC_URL_FORMAT.format(info['id']), 'caption': info['caption'],
                              'label': info['label']}
                data['photos'].append(photo_dict)
            return JsonResponse(CustomResponseJson(msg='获取餐厅图片成功', code=1, data=data).__str__())
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID错误', code=0).__str__())
    return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0).__str__())


def tips_info(request):
    if request.method == 'GET':
        restaurant_id = request.GET.get('id', None)
        if restaurant_id is not None:
            count = Tip.objects.filter(restaurant_id=restaurant_id).count()
            data = dict(tips_num=count, tips=list(
                Tip.objects.filter(restaurant_id=restaurant_id).order_by('?')[:5].values('id', 'user_id', 'custom_user',
                                                                                         'text', 'date', 'likes')))
            return JsonResponse(CustomResponseJson(msg='查询餐厅简评成功', code=1, data=data).__str__())
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID错误', code=0).__str__())
    return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0).__str__())


def review_info(request):
    if request.method == 'GET':
        restaurant_id = request.GET.get('id', None)
        current_page = request.GET.get('page', 1)
        order = request.GET.get('order', 1)
        if restaurant_id is not None:
            if str(order) == '1':
                order = '-'
            else:
                order = ''
            reviews = Review.objects.filter(restaurant_id=restaurant_id).order_by(order + 'date').values()
            pages = Paginator(reviews, 10)
            try:
                reviews = pages.page(current_page)
                data = dict(reviews_sum=pages.count, page_num=pages.num_pages, has_pre=reviews.has_previous(),
                            has_next=reviews.has_next(), reviews_this_page=len(reviews), reviews=list(reviews))
                return JsonResponse(CustomResponseJson(
                    msg='获取餐厅第{0}页评价成功'.format(current_page), code=1, data=data).__str__())
            except EmptyPage as e:
                return JsonResponse(CustomResponseJson(msg='页码错误,{0}'.format(e), code=0).__str__())
        return JsonResponse(CustomResponseJson(msg='传入餐厅ID错误', code=0).__str__())
    return JsonResponse(CustomResponseJson(msg='调用方法错误', code=0).__str__())


def recommend(request):
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
            return JsonResponse(CustomResponseJson('请求成功', 1, restaurants_values_list).__str__())
        else:
            return JsonResponse(CustomResponseJson('传入参数错误', 0).__str__())
    else:
        return JsonResponse(CustomResponseJson('传入参数错误', 0).__str__())
