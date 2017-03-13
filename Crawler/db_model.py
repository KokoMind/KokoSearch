"""This file contain the database caching model"""
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

DB_CRAWLER = SqliteExtDatabase('Crawler_cache.db')


class BaseModel(Model):
    class Meta:
        database = DB_CRAWLER


class Crawled(BaseModel):
    id = PrimaryKeyField()
    thread_id = IntegerField()
    url = CharField(unique=True)
    dns = CharField()
    content = TextField()
    visited = DateTimeField()
    last_visit = DateTimeField()
    indexed = BooleanField()
    last_indexed = DateTimeField(null = True)


class ToCrawl(BaseModel):
    url = TextField()
    dns = CharField()
    value = DoubleField()


class Hasher(BaseModel):
    hash = CharField(max_length=42, unique=True, index=True, null=False)


def create_database():
    DB_CRAWLER.connect()
    DB_CRAWLER.create_tables([Crawled, ToCrawl, Hasher], safe=True)

# create the database and the schema
# create_database()
