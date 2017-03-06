from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('Indexer_cache.db')


class BaseModel(Model):
    class Meta:
        database = db


class Word(BaseModel):
    word = CharField(unique=True)
    num_of_docs = IntegerField()


class Topic(BaseModel):
    num_of_docs = IntegerField()


class Document(BaseModel):
    url = CharField(unique=True)
    c1 = ForeignKeyField(Topic, related_name='c1')
    c2 = ForeignKeyField(Topic, related_name='c2')
    c3 = ForeignKeyField(Topic, related_name='c3')
    c4 = ForeignKeyField(Topic, related_name='c4')
    c5 = ForeignKeyField(Topic, related_name='c5')


class Word_Doc(BaseModel):
    doc_id = ForeignKeyField(Document, related_name='doc_id')
    word_id = ForeignKeyField(Word, related_name='word_id')
    pos = IntegerField()
    neighbours = CharField()


def create_data_base():
    db.connect()
    db.create_tables([Document, Word_Doc, Word, Topic], safe=True)
