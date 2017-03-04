from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Word(BaseModel):
    word = CharField()
    num_of_docs = IntegerField()


class Topic(BaseModel):
    num_of_docs = IntegerField()


class Document(BaseModel):
    url = CharField()


class Word_Doc(BaseModel):
    doc_id = ForeignKeyField(Document, related_name='words')
    word_id = ForeignKeyField(Word, related_name='docs')
    pos = IntegerField()
    neighbours = CharField()


def create_data_base():
    db.connect()
    db.create_tables([Document, Word_Doc, Word, Topic])



create_data_base()