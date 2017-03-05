from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('Crawler_cache.db')


class BaseModel(Model):
    class Meta:
        database = db


class Crawled(BaseModel):
    url = CharField(unique=True)
    content = TextField()
    refresh = IntegerField()


class ToCrawl(BaseModel):
    url = CharField()


def create_data_base():
    db.connect()
    db.create_tables([Crawled, ToCrawl], safe=True)
