import threading
from aptdaemon import lock
from Crawler import frontier
from Crawler.fetcher import Fetcher
from Crawler.db_worker import DBCacheCrawled


class CrawlerThread(threading.Thread):
    """Class of a thread to crawl the web"""

    def __init__(self, thread_id, name, frontier_):
        """Construct a new crawling thread"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.frontier = frontier_

    def run(self):
        """The starting point of a thread"""
        print("Thread " + str(self.thread_id) + " started")
        while True:
            # print("get next URL")
            value, current_URL = self.frontier.get_url(self.thread_id)
            if not current_URL:
                print("Empty Queue from thread " + str(self.thread_id))
                continue
            print("URL got from thread " + str(self.thread_id))
            code, links, content = Fetcher.fetch(current_URL)
            if code == -1:
                print("Error 2 from thread " + str(self.thread_id))
                continue
            out_links = len(links)
            sz_parent = len(content)
            links_mod = []
            for i in range(len(links)):
                links_mod.append((links[i][0], links[i][1], (out_links, sz_parent, len(links[i][0]), value)))

            print("URL fetched from thread " + str(self.thread_id))
            # lock.acquire()
            self.frontier.push_to_serve(links_mod)
            # lock.release()
            DBCacheCrawled(0, 'cache_crawled', self.thread_id, self.name, 0, current_URL, content).start()
            print("URL cached  from thread " + str(self.thread_id))
