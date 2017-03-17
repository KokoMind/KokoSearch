import threading
from fetcher import Fetcher
from db_worker import DBCacheCrawled, DBDeleteCrawled, DBCacheCrawledRevisit


class CrawlerThread(threading.Thread):
    """Class of a thread to crawl the web"""

    def __init__(self, thread_id, name, frontier_, dash_):
        """Construct a new crawling thread"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.daemon = True
        self.name = name
        self.frontier = frontier_
        self.dash = dash_
        self.crawled = 0
        self.threadlock = threading.Lock()

    def run(self):
        """The starting point of a thread"""
        # print("Thread " + str(self.thread_id) + " started")
        while True:
            # print("get next URL")
            self.dash.print_cur_stat("Get next url", self.thread_id)
            value, current_url, current_dns = self.frontier.get_url(self.thread_id)
            if not current_url:
                # print("Empty Queue from thread " + str(self.thread_id))
                self.dash.print_cur_stat("Empty Queue", self.thread_id)
                continue
            self.dash.print_cur_stat("Downloading...", self.thread_id)
            code, links, content = Fetcher.fetch(current_url)
            if code == -1:
                # print("Refused from thread " + str(self.thread_id))
                self.dash.print_cur_stat("Refused url", self.thread_id)
                continue
            self.dash.print_cur_stat("Accepted url", self.thread_id)
            # Crawling this link successeded
            # print("URL got from thread " + str(self.thread_id))
            out_links = len(links)
            sz_parent = len(content)
            links_mod = []
            for i in range(len(links)):
                links_mod.append((links[i][0], links[i][1], (out_links, sz_parent, len(links[i][0]), value)))

            self.dash.print_cur_stat("URL fetched", self.thread_id)
            self.crawled += 1
            self.dash.print_crawled(str(self.crawled), self.thread_id)
            # print("URL fetched from thread " + str(self.thread_id))
            self.frontier.push_to_serve(links_mod, self.thread_id)
            DBCacheCrawled(0, 'cache_crawled', self.thread_id, self.name, 0, current_url, current_dns, content, self.thread_id).start()
            # print("URL cached  from thread " + str(self.thread_id))
            # self.dash.print_cur_stat("Cached link", self.thread_id)


class RevisiterThread(threading.Thread):
    """Class of a thread to crawl the web"""

    def __init__(self, thread_id, name, frontier_):
        """Construct a new crawling thread"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.frontier = frontier_
        self.threadlock = threading.Lock()

    def run(self):
        """The starting point of a thread"""
        print("Thread " + str(self.thread_id) + " started")
        while True:
            uid, current_url = self.frontier.get_url(self.thread_id)
            if not current_url:
                break
            print("thread " + str(self.thread_id) + " Got a URL")
            code, _, content = Fetcher.fetch(current_url)
            if code == -1:
                print("Unable to fetch link from thread " + str(self.thread_id))
                DBDeleteCrawled(0, 'cache_crawled', self.thread_id, self.name, 0, uid).start()
                continue
            print("URL Refreshed from thread " + str(self.thread_id))
            DBCacheCrawledRevisit(0, 'cache_crawled', self.thread_id, self.name, 0, uid, content).start()
        print(self.name + " has finished revisiting")
