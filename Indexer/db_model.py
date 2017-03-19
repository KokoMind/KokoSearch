from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase(':memory:')
db_disk = SqliteExtDatabase('./Indexer_disk.db')


# Memory Database
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


class Word_Doc(BaseModel):
    doc_id = ForeignKeyField(Document, related_name='doc_id')
    word_id = ForeignKeyField(Word, related_name='word_id')
    pos = IntegerField()
    neighbours = CharField()


# Disk Database
class BaseModelDisk(Model):
    class Meta:
        database = db_disk


class WordDisk(BaseModelDisk):
    word = CharField(unique=True)
    num_of_docs = IntegerField()


class TopicDisk(BaseModelDisk):
    num_of_docs = IntegerField()


class DocumentDisk(BaseModelDisk):
    url = CharField(unique=True)
    c1 = ForeignKeyField(TopicDisk, related_name='c1')
    c2 = ForeignKeyField(TopicDisk, related_name='c2')
    c3 = ForeignKeyField(TopicDisk, related_name='c3')
    c4 = ForeignKeyField(TopicDisk, related_name='c4')
    c5 = ForeignKeyField(TopicDisk, related_name='c5')


class Word_DocDisk(BaseModelDisk):
    doc_id = ForeignKeyField(DocumentDisk, related_name='doc_id')
    word_id = ForeignKeyField(WordDisk, related_name='word_id')
    pos = IntegerField()
    neighbours = CharField()


def create_data_base():
    db.connect()
    db.create_tables([Document, Word_Doc, Word, Topic], safe=True)
    db_disk.connect()
    db_disk.create_tables([DocumentDisk, Word_DocDisk, WordDisk, TopicDisk], safe=True)
