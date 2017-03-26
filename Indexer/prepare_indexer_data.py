from pymongo import MongoClient
import pymongo


def prepare():
    crawler_db = MongoClient()['crawled']
    crawled = crawler_db['crawled']
    crawled.create_index([('page_id', pymongo.ASCENDING)], unique=True)

    for i, s in enumerate(crawled.find()):
        crawled.update_one({'_id': s['_id']}, {'$inc': {'my_id_1': i}})
        if i % 10000 == 0:
            print(i)


prepare()
