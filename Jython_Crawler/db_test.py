"""File to test database transactions"""

from storage import *
from db_worker import *
import logging

# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

db = Storage()

# ret1 = Storage.cache_crawled_url('www.google.com' + datetime.now().isoformat(), '5lty')
# ret2 = Storage.cache_hash('www.google.com' + datetime.now().isoformat())
# ret3 = Storage.cache_to_crawl([(0.1, 'www.google.com1', '192.168.1.1')])
# ret4, links = Storage.get_to_crawl()
#
# print(links)
# print(ret1)
# print(ret2)
# print(ret3)
# print(ret4)
#
# assert ret1 == 0
# assert ret2 == 0
# assert ret3 == 0
# assert ret4 == 0
#
# assert Storage.cache_crawled_url('www.google.com', '5lty') == -1
# assert Storage.cache_hash('www.google.com') == 1

DBCacheCrawled(0, '', 0, '', 1, 'www.moemen.com', '5lty').start()
print("Exiting Main Thread")
