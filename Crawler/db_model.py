from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('Crawler_cache.db')


class BaseModel(Model):
    class Meta:
        database = db


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
    db.connect()
    db.create_tables([Crawled, ToCrawl, Hasher], safe=True)
