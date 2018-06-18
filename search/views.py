from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from search.models import RestaurantType
from rrsite.util.json import CustomResponseJson
from rrsite.util.restaurant import get_cover
from RRWeb.settings import PHOTO_STATIC_URL_FORMAT

from elasticsearch_dsl import Search
from datetime import datetime


def search_result(request):
    return render(request, 'search/search.html', context=dict(username=request.session.get('username', '')))


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        if not key_words:
            return JsonResponse(CustomResponseJson('关键词不能为空', code=0))
        data = list()
        s = RestaurantType.search()
        s = s.suggest(name='suggestion', text=key_words, completion=dict(
            field='suggest',
            fuzzy=dict(
                fuzziness=1
            ),
            size=10
        ))
        suggestions = s.execute()

        for match in suggestions.suggest.suggestion[0].options:
            restaurant_id = match['_id']
            name = match['_source']['name']
            address = match['_source']['address']
            city = match['_source']['city']
            category = match['_source']['category']
            if restaurant_id is not None and name is not None:
                data.append(dict(id=restaurant_id, name=name, address=address, city=city, category=list(category)))
        return JsonResponse(CustomResponseJson(msg='查询建议成功', code=1, data=data))


class CityAddressSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        if not key_words:
            return JsonResponse(CustomResponseJson('关键词不能为空', code=0))
        data = list()
        s = RestaurantType.search()
        s = s.suggest(name='suggestion', text=key_words, completion=dict(
            field='suggest_city',
            fuzzy=dict(
                fuzziness=0
            ),
            size=10
        ))
        suggestions = s.execute()
        for match in suggestions.suggest.suggestion[0].options:
            address = match['_source']['address']
            city = match['_source']['city']
            data.append(dict(address=address, city=city))
        return JsonResponse(CustomResponseJson(msg='查询建议成功', code=1, data=data))


class SearchView(View):
    def get(self, request):
        # 获取关键词参数
        key_words = request.GET.get('s', None)
        city = request.GET.get('city', None)
        lat = request.GET.get('lat', None)
        lon = request.GET.get('lon', None)
        price_range = request.GET.get('pricerange', None)
        page = request.GET.get('p', 1)
        try:
            page = int(page)
        except ValueError:
            page = 1
        query_dict = {
            'query': {
                'bool': {
                    'filter': [],
                    'must': []
                }
            },
            'from': 10 * (page - 1),
            'size': 10,
            '_source': [
                'name', 'address', 'city', 'state', 'postal_code', 'neighborhood', 'stars', 'review_count',
                'location', 'is_open', 'attribute.*', 'category'
            ],
            'highlight': {
                'fields': {
                    'name': {}
                },
                'pre_tags': '<span class="">',
                'post_tags': '</span>'
            }
        }
        if key_words:
            query_dict['query']['bool']['must'].append(
                dict(multi_match={
                    'query': key_words,
                    'fields': ['name^3', 'category'],
                    'boost': 2.0
                }))

        if city:
            city = str(city).replace('-', ' ')
            query_dict['query']['bool']['must'].append(
                dict(multi_match={
                    'query': city,
                    'fields': ['city^3', 'address'],
                    'boost': 1.0
                }))

        if price_range:
            query_dict['query']['bool']['filter'].append(
                dict(
                    nested={
                        'path': 'attribute',
                        'score_mode': 'avg',
                        'query': {
                            'bool': {
                                'must': [
                                    {'match': {'attribute.RestaurantsPriceRange2': price_range}}
                                ]
                            }
                        }
                    }
                )
            )

        try:
            if lat and lon:
                lat = float(lat)
                lon = float(lon)
                query_dict['query']['bool']['filter'].append(
                    dict(geo_distance={
                        'location': [lon, lat],
                        'distance': '20km'
                    }))
        except ValueError:
            return JsonResponse(CustomResponseJson('位置信息错误', code=0))
        start_time = datetime.now()
        try:
            s = Search.from_dict(query_dict)
            response = s.execute()
        except ConnectionError:
            return JsonResponse(CustomResponseJson(msg='搜索失败', code=0))

        end_time = datetime.now()
        last_time = (end_time - start_time).total_seconds()
        total_nums = response['hits']['total']
        if total_nums % 10 > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)

        if page < total_nums:
            has_next = True
        else:
            has_next = False

        hit_list = response.hits.hits
        restaurant_list = list()
        data = dict(
            last_time=last_time, page_nums=page_nums,
            key_words=key_words, total_nums=total_nums,
            data=restaurant_list, has_next=has_next
        )
        for hit_dict in hit_list:
            restaurant_id = hit_dict.get('_id', None)
            cover_id = get_cover(restaurant_id)
            if cover_id:
                cover_url = PHOTO_STATIC_URL_FORMAT.format(str(cover_id))
            else:
                cover_url = 'http://58.87.109.246/static/rrsite/default-cover.jpg'
            restaurant_info = hit_dict.get('_source', None)
            restaurant_info['id'] = restaurant_id
            restaurant_info['cover_url'] = cover_url
            highlight = hit_dict.get('highlight', None)
            if highlight:
                name = highlight.get('name', None)
                if name is not None:
                    restaurant_info['name'] = name[0]
            restaurant_list.append(restaurant_info)
        return JsonResponse(CustomResponseJson(msg='搜索成功', code=1, data=data))
