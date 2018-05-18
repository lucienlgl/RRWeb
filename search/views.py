from django.http import JsonResponse
from django.views.generic import View

from search.models import RestaurantType
from rrsite.util.json import CustomResponseJson
from elasticsearch_dsl.query import Q

from datetime import datetime


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
                fuzziness=2
            ),
            size=10
        ))
        suggestions = s.execute()

        for match in suggestions.suggest.suggestion[0].options:
            restaurant_id = match.get('_id', None)
            name = match['_source'].get('name', None)
            if restaurant_id is not None and name is not None:
                data.append(dict(id=restaurant_id, name=name))
        return JsonResponse(CustomResponseJson(msg='查询建议成功', code=1, data=data))


class SearchView(View):
    def get(self, request):
        # 获取关键词参数
        key_words = request.GET.get('s', '')
        # 获取页码
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except ValueError:
            page = 1
        if not key_words:
            return JsonResponse(CustomResponseJson('关键词不能为空', code=0))
        start_time = datetime.now()

        # 搜索elasticsearch
        s = RestaurantType.search()
        # 多重搜索name和address
        s = s.query(Q('multi_match', query=key_words, fields=['name^5', 'address']))
        # 高亮关键词，用于填充模板
        s = s.highlight_options(pre_tags='<em>', post_tags='</em>')
        s = s.highlight('name')
        s = s.highlight('address')
        # 获取当前页
        s = s[page - 1: 10]
        # 只保留以下字段
        s = s.source(fields=['name', 'address', 'city', 'state', 'postal_code', 'neighborhood', 'stars', 'review_count',
                             'location', 'is_open'])
        response = s.execute()
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
        data = dict(last_time=last_time, page_nums=page_nums, key_words=key_words, total_nums=total_nums,
                    data=restaurant_list, has_next=has_next)
        for hit_dict in hit_list:
            restaurant_id = hit_dict.get('_id', None)
            restaurant_info = hit_dict.get('_source', None)
            highlight = hit_dict.get('highlight', None)
            if restaurant_info is not None and restaurant_id is not None and highlight is not None:
                restaurant_info['id'] = restaurant_id
                name = highlight.get('name', None)
                address = highlight.get('address', None)
                if name is not None:
                    restaurant_info['name'] = name[0]
                if address is not None:
                    restaurant_info['address'] = address[0]
                restaurant_list.append(restaurant_info)
        return JsonResponse(CustomResponseJson(msg='搜索成功', code=1, data=data))
