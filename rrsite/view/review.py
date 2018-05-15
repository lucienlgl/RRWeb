from django.http import JsonResponse

from rrsite.models import Photo, Restaurant, Review
from rrsite.util.json import CustomResponseJson
from RRWeb.settings import PHOTO_STATIC_URL_FORMAT


def hot_review(request):
    if request.method == 'GET' or request.method == 'HEAD':
        restaurants_values_list = list(Restaurant.objects.filter(review_count__gte=500).order_by('?')[:5].values())
        review_list = []
        for restaurant_dict in restaurants_values_list:
            review_dict = Review.objects.filter(restaurant_id=restaurant_dict.get('id', None))[:1]. \
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
        return JsonResponse(CustomResponseJson('请求成功', 1, review_list))
    else:
        return JsonResponse(CustomResponseJson('请求方法错误', 0))
