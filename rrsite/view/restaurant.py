from django.http import JsonResponse

from rrsite.models import Photo, Restaurant
from rrsite.util.json import CustomResponseJson
from RRWeb.settings import PHOTO_STATIC_URL_FORMAT


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
            return JsonResponse(CustomResponseJson('请求成功', 1, restaurants_values_list).__str__())
        else:
            return JsonResponse(CustomResponseJson('传入参数错误', 0).__str__())
    else:
        return JsonResponse(CustomResponseJson('传入参数错误', 0).__str__())
