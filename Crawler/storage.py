"""File to handle all database transactions"""

from Crawler.db_model import *
from datetime import datetime
import hashlib


class Storage:
    """This class handles database transactions and contain the temporary lists"""

    def __init__(self):
        DB_CRAWLER.connect()

    def __del__(self):
        DB_CRAWLER.close()

    @staticmethod
    @DB_CRAWLER.transaction()
    def cache_crawled_url(url, dns, content, thread_id):
        """save a crawled link return 0 if successfull -1 if database error"""
        try:
            with DB_CRAWLER.atomic():
                Crawled.create(thread_id=thread_id, url=url, dns=dns, content=content, indexed=False, visited=datetime.now().isoformat())
            return 0
        except DatabaseError:
            return -1

    @staticmethod
    @DB_CRAWLER.transaction()
    def cache_hash(url):
        """save the hash of a url return 0 if successfull -1 if database error 0 if already found"""
        try:
            with DB_CRAWLER.atomic():
                Hasher.create(hash=hashlib.sha1(url.encode('ascii', 'ignore')).hexdigest())
            return 0
        except IntegrityError:
            return 1
        except DatabaseError:
            return -1

    @staticmethod
    @DB_CRAWLER.transaction()
    def cache_to_crawl(to_crawl_list):
        """to_crawl_list must be [(value, url, dns),...] cache to crawl lists return 0 if successfull -1 if database error"""
        data_source = [{'url': url, 'dns': dns, 'value': value} for value, url, dns in to_crawl_list]
        try:
            with DB_CRAWLER.atomic():
                for idx in range(0, len(data_source), 100):
                    ToCrawl.insert_many(data_source[idx:idx + 100]).execute()
            return 0
        except DatabaseError:
            return -1

    @staticmethod
    @DB_CRAWLER.transaction()
    def get_to_crawl(no=None):
        """retrieve links to continue crawling no? for specific number of links return [(value,url,dns),...]"""
        try:
            if not no:
                links = [(link.value, link.url, link.dns) for link in ToCrawl.select()]
            else:
                links = [(link.value, link.url, link.dns) for link in ToCrawl.select().paginate(1, no)]
            return 0, links
        except DatabaseError:
            return -1, None
