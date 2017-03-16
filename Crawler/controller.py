from Crawler.frontier import Frontier, FrontierRevisit
from Crawler.worker import CrawlerThread, RevisiterThread
from Crawler.storage import Storage


class Controller:
    """The Controller of the hole Crawling process"""

    def __init__(self, num_threads, seeds, cont_to_crawl):
        self.num_workers = num_threads
        self.workers = []
        self.frontier = Frontier(num_threads)
        self.db = Storage()
        # Create the workers
        for i in range(num_threads):
            self.workers.append(CrawlerThread(i, 'CrawlerThread' + str(i), self.frontier))
        print("Workers created")
        # insert seeds in to serve
        if not cont_to_crawl:
            self.frontier.push_to_serve(seeds, 0)
            print("seeds pushed")
            self.frontier.distribute()
            print("seeds distributed")
        else:
            self.frontier.load_to_crawl()

    def run(self):
        """The main Program"""
        try:
            for i in range(self.num_workers):
                self.workers[i].start()
            print("All Workers started")
            while True:
                self.frontier.distribute()
        except KeyboardInterrupt:
            print("saving before exit")
            self.frontier.save_to_crawl()


class ControllerRevisit:
    """The Controller of the hole Revisiting process"""

    def __init__(self, num_threads):
        self.num_workers = num_threads
        self.workers = []
        self.frontier = FrontierRevisit(num_threads)
        self.db = Storage()
        # Create the workers
        for i in range(num_threads):
            self.workers.append(RevisiterThread(i, 'CrawlerThread' + str(i), self.frontier))
        print("Workers created")

    def run(self):
        """The main Program"""
        try:
            self.frontier.distribute()
            for i in range(self.num_workers):
                self.workers[i].start()
            print("All Workers started")
            for i in range(self.num_workers):
                self.workers[i].join()
            print("All Workers Finished")
        except KeyboardInterrupt:
            print("Program Interrupted")
