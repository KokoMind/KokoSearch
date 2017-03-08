import threading
from aptdaemon import lock


class CrawlerThread(threading.Thread):
    """Class of a thread to crawl the web"""

    def __init__(self, thread_id, name):
        """Construct a new crawling thread"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        """The starting point of a thread"""
        lock.acquire()
        #Here call the insertion to frontier queue.
        lock.release()
