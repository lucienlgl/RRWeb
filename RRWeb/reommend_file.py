import MySQLdb


if __name__ == '__main__':
    sql = """SELECT restaurant_id, custom_user_id, user_id, stars, `date` FROM review LIMIT 500000"""
    db = MySQLdb.connect(host='58.87.109.246', user='root', passwd='lglmmd', db='rrweb_db', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sql)
    reviews = cursor.fetchall()
    with open('reviews.txt', 'w') as f:
        for review in reviews:
            if review[2]:
                user_id = review[2]
            else:
                user_id = review[1]
            f.write('%s\t%s\t%s\t%s\n' % (review[0], user_id, review[3], str(review[4]).replace('-', '')))
        f.close()
    cursor.close()
    db.close()
