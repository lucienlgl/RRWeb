from elasticsearch_dsl import DocType, Boolean, \
    Completion, Keyword, Text, Integer, Double, GeoPoint, Nested

import elasticsearch_dsl.analysis
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['127.0.0.1:9200'])


class CustomAnalyzer(elasticsearch_dsl.analysis.CustomAnalyzer):
    def get_analysis_definition(self):
        return dict()


eng_analyzer = CustomAnalyzer('english', filter=['lowercase'])


class RestaurantType(DocType):
    name = Text(analyzer='english')
    address = Text(analyzer='english')
    neighborhood = Text(analyzer='english')
    city = Keyword()
    postal_code = Keyword()
    state = Keyword()
    stars = Double()
    location = GeoPoint()
    review_count = Integer()
    is_open = Boolean()
    hours = Nested()
    attribute = Nested()

    suggest = Completion(analyzer=eng_analyzer)
    suggest_city = Completion(analyzer=eng_analyzer)

    class Meta:
        index = 'rrweb'
        doc_type = 'restaurant'


if __name__ == '__main__':
    RestaurantType.init()
