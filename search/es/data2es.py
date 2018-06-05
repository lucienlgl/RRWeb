from search.models import RestaurantType
import MySQLdb
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch

es = connections.create_connection(RestaurantType._doc_type.using)

db = MySQLdb.connect(host="127.0.0.1", user='root', password='12345678', port=3306, db="rrweb_db")


def generate_suggest(index, info_tuple):
    used_words = set()
    suggests = []
    new_words = set()
    for info, weight in info_tuple:
        if info and isinstance(info, str):
            info = [info]
        for text in info:
            response = es.indices.analyze(
                index=index,
                params=dict(
                    filter=['lowercase']
                ),
                body=dict(
                    analyzer='english',
                    text=text
                )
            )
            analyzed_words = set(r['token'] for r in response['tokens'] if len(r['token']) > 1)
            new_words = analyzed_words - used_words
        if new_words:
            suggests.append(dict(input=list(new_words), weight=weight))

    return suggests


if __name__ == '__main__':
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = """SELECT * FROM restaurant"""
    sql_category = """SELECT `category` FROM `category` WHERE restaurant_id = %s"""
    sql_hours = """SELECT `day`, `hours` FROM `hour` WHERE restaurant_id = %s"""
    sql_attribute = """SELECT `name`, `value` FROM `attribute` WHERE restaurant_id = %s"""

    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:

        restaurant_dict = dict(
            name=row[1],
            neighborhood=row[2],
            address=row[3],
            city=row[4],
            state=row[5],
            postal_code=row[6],
            location=dict(lat=row[7], lon=row[8]),
            stars=row[9],
            review_count=row[10],
            is_open=row[11],
            category=[],
            hours={},
            attribute={},
            suggest=[],
            suggest_city=[]
        )

        cursor.execute(sql_category, (row[0],))
        categories = cursor.fetchall()
        [restaurant_dict['category'].append(category[0]) for category in categories]

        cursor.execute(sql_hours, (row[0],))
        hours = cursor.fetchall()
        hours_dict = dict()
        for hour in hours:
            hours_dict[hour[0]] = hour[1]
        restaurant_dict['hours'] = hours_dict

        cursor.execute(sql_attribute, (row[0],))
        attributes = cursor.fetchall()
        attributes_dict = dict()
        for attribute in attributes:
            name = attribute[0]
            value = attribute[1]
            if '_' not in name:
                attributes_dict[name] = value
            else:
                main_sub = str(name).split('_')
                if main_sub[0] not in attributes_dict:
                    attributes_dict[main_sub[0]] = dict()
                    attributes_dict[main_sub[0]][main_sub[1]] = value
                else:
                    attributes_dict[main_sub[0]][main_sub[1]] = value
        restaurant_dict['attribute'] = attributes_dict

        restaurant_dict['suggest'] = generate_suggest(
            RestaurantType._doc_type.index,
            ((restaurant_dict['name'], 10), (restaurant_dict['category'], 5))
        )

        restaurant_dict['suggest_city'] = generate_suggest(
            RestaurantType._doc_type.index,
            ((restaurant_dict['city'], 10), (restaurant_dict['address'], 7))
        )

        elasticsearch = Elasticsearch(['localhost'])
        elasticsearch.create(index='rrweb', doc_type='restaurant', id=row[0], body=restaurant_dict)

db.close()
