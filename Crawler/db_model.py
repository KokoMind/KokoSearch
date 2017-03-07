from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

DB_CRAWLER = SqliteExtDatabase('Crawler_cache.db')


class BaseModel(Model):
    class Meta:
        database = DB_CRAWLER


class Crawled(BaseModel):
    url = CharField(unique=True)
    content = TextField()
    indexed = BooleanField()
    visited = DateTimeField()


class ToCrawl(BaseModel):
    url = TextField()
    dns = CharField()
    value = DoubleField()


class Hasher(BaseModel):
    hash = CharField(max_length=21, unique=True, index=True, null=False)


def create_data_base():
    DB_CRAWLER.connect()
    DB_CRAWLER.create_tables([Crawled, ToCrawl, Hasher], safe=True)
