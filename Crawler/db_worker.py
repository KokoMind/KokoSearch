import threading
from Crawler.storage import *


class DBWorker(threading.Thread):
    """Class for a thread which will do a specific task in database"""

    def __init__(self, thread_id, name, parent_id, parent_name, *args, verbose=0):
        """Construct a new db thread"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.parent_id = parent_id
        self.parent_name = parent_name
        self.verbose = verbose
        self.args = args


class DBCacheCrawled(DBWorker):
    def run(self):
        if self.verbose:
            if Storage.cache_crawled_url(*self.args) == 0:  # Successfull
                print("Crawled link is saved successfully from parent " + self.parent_name)
            else:
                print("Error for saving crawled link")
        pass
