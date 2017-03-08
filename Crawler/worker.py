import threading
from aptdaemon import lock
from Crawler import frontier
from Crawler.fetcher import Fetcher
from Crawler.db_worker import DBCacheCrawled

class CrawlerThread(threading.Thread):
    """Class of a thread to crawl the web"""

    def __init__(self, thread_id, name,frontier):
        """Construct a new crawling thread"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.frontier = frontier

    def run(self):
        """The starting point of a thread"""
        while True:
            current_URL = frontier.get_url()
            code, links, content = Fetcher.fetch(current_URL)
            if code == -1:
                continue
            lock.acquire()
            frontier.push_to_serve(links)
            lock.release()
            DBCacheCrawled(0, 'cache_crawled', self.thread_id, self.name, 0, current_URL, content).start()

