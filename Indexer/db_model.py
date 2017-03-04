from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Word(BaseModel):
    id = IntegerField(unique=True)
    word = CharField( )
    num_of_docs = IntegerField( )


class Topics(BaseModel):
    id = IntegerField(unique=True)
    num_of_docs = IntegerField( )


def create_data_base():
    db.connect()
    db.create_tables([Document,Word_Doc,Word, Topics])