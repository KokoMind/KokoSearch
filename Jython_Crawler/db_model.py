"""This file contain the database caching model"""
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

DB_CRAWLED = SqliteExtDatabase('crawled_cache.db')
DB_HASHER = SqliteExtDatabase('hasher_cache.db')
DB_TOCRAWL = SqliteExtDatabase('tocrawl_cache.db')


class BaseModelCrawled(Model):
    class Meta:
        database = DB_CRAWLED


class BaseModelHasher(Model):
    class Meta:
        database = DB_HASHER


class BaseModelToCrawl(Model):
    class Meta:
        database = DB_TOCRAWL


class Crawled(BaseModelCrawled):
    id = PrimaryKeyField()
    thread_id = IntegerField()
    url = CharField(unique=True)
    dns = CharField()
    content = TextField()
    visited = DateTimeField()
    last_visit = DateTimeField()
    indexed = BooleanField()
    last_indexed = DateTimeField(null=True)


class ToCrawl(BaseModelToCrawl):
    url = TextField()
    dns = CharField()
    value = DoubleField()


class Hasher(BaseModelHasher):
    hash = CharField(max_length=42, unique=True, index=True, null=False)


def create_database():
    DB_CRAWLED.connect()
    DB_HASHER.connect()
    DB_TOCRAWL.connect()
    DB_CRAWLED.create_tables([Crawled], safe=True)
    DB_HASHER.create_tables([Hasher], safe=True)
    DB_TOCRAWL.create_tables([ToCrawl], safe=True)
    DB_CRAWLED.close()
    DB_HASHER.close()
    DB_TOCRAWL.close()


# create the database and the schema
# create_database()

if __name__ == '__main__':
    create_database()
