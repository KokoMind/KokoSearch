"""File to handle all database transactions"""

from db_model import *
from datetime import datetime
import hashlib


class Storage:
    """This class handles database transactions and contain the temporary lists"""

    def __init__(self):
        DB_CRAWLED.connect()
        DB_HASHER.connect()
        DB_TOCRAWL.connect()

    def __del__(self):
        DB_CRAWLED.close()
        DB_HASHER.close()
        DB_TOCRAWL.close()

    @staticmethod
    @DB_CRAWLED.transaction()
    def cache_crawled_url(url, dns, content, thread_id):
        """save a crawled link return 0 if successfull -1 if database error"""
        try:
            with DB_CRAWLED.atomic():
                Crawled.create(thread_id=thread_id, url=url, dns=dns, content=content, visited=datetime.now().isoformat(), last_visit=datetime.now().isoformat(), indexed=False)
            return 0
        except:
            return -1

    @staticmethod
    @DB_HASHER.transaction()
    def cache_hash(url):
        """save the hash of a url return 0 if successfull -1 if database error 0 if already found"""
        try:
            with DB_HASHER.atomic():
                Hasher.create(hash=hashlib.sha1(url.encode('ascii', 'ignore')).hexdigest())
            return 0
        except IntegrityError:
            return 1
        except:
            return -1

    @staticmethod
    @DB_TOCRAWL.transaction()
    def cache_to_crawl(to_crawl_list):
        """to_crawl_list must be [(value, url, dns),...] cache to crawl lists return 0 if successfull -1 if database error"""
        data_source = [{'url': url, 'dns': dns, 'value': value} for value, url, dns in to_crawl_list]
        try:
            with DB_TOCRAWL.atomic():
                for idx in range(0, len(data_source), 100):
                    ToCrawl.insert_many(data_source[idx:idx + 100]).execute()
            return 0
        except:
            return -1

    @staticmethod
    @DB_TOCRAWL.transaction()
    def get_to_crawl(page=None, no=1000):
        """retrieve links to continue crawling no? for specific number of links return [(value,url,dns),...]"""
        try:
            if not page:
                links = [(link.value, link.url, link.dns) for link in ToCrawl.select()]
            else:
                links = [(link.value, link.url, link.dns) for link in ToCrawl.select().paginate(page, no)]
            return 0, links
        except:
            return -1, None

    @staticmethod
    @DB_TOCRAWL.transaction()
    def delete_to_crawl():
        try:
            DB_TOCRAWL.execute_sql("delete from tocrawl")
            return 0
        except:
            return -1

    @staticmethod
    @DB_CRAWLED.transaction()
    def get_crawled(page=None, no=1000):
        """retrieve links to revisit return [(id,url)]"""
        try:
            if not page:
                links = [(link.id, link.url) for link in Crawled.select()]
            else:
                links = [(link.id, link.url) for link in Crawled.select().paginate(page, no)]
            return 0, links
        except:
            return -1, None

    @staticmethod
    @DB_CRAWLED.transaction()
    def cache_crawled_revisit(uid, content):
        """save a crawled link return 0 if successfull -1 if database error"""
        try:
            with DB_CRAWLED.atomic():
                query = Crawled.update(content=content, last_visit=datetime.now().isoformat()).where(Crawled.id == uid)
                query.execute()
            return 0
        except:
            return -1

    @staticmethod
    @DB_CRAWLED.transaction()
    def delete_crawled_link(uid):
        try:
            with DB_CRAWLED.atomic():
                query = Crawled.delete().where(Crawled.id == uid)
                query.execute()
            return 0
        except:
            return -1
