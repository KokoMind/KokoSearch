from pymongo import MongoClient
import pymongo


def prepare():
    crawler_db = MongoClient()['crawled']
    crawled = crawler_db['crawled']
    result = crawled.create_index([('page_id', pymongo.ASCENDING)], unique=True)


test_db = MongoClient()['test']
test = test_db['test']

test.create_index([('my_id', pymongo.ASCENDING)])

print(sorted(list(test.index_information())))

for i, s in enumerate(test.find()):
    test.update_one({'_id': s['_id']}, {'$inc': {'my_id_1': i}})
    if i % 10000 == 0:
        print(i)

print(test.find({'my_id_1': 0})[0])
