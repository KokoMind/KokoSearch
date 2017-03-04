from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Word(BaseModel):
    id = IntegerField(unique=True)
    word = CharField()
    num_of_docs = IntegerField()


class Topics(BaseModel):
    id = IntegerField(unique=True)
    num_of_docs = IntegerField()


class Document(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    url = CharField()


class Word_Doc(BaseModel):
    id = CharField(unique=True, primary_key=True)
    doc_id = ForeignKeyField(Document, related_name='words')
    word_id = ForeignKeyField(Word, related_name='docs')
    pos = IntegerField()
    neighbours = CharField()


def create_data_base():
    db.connect()
    db.create_tables([Document, Word_Doc, Word, Topics])
