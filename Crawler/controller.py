from Crawler.frontier import Frontier
from Crawler.worker import CrawlerThread


class Controller:
    """The Controller of the hole Crawling process"""

    def __init__(self, num_threads):
        self.num_workers = num_threads
        self.workers = []
        self.frontier = Frontier(num_threads)
        # Create the workers
        for i in range(num_threads):
            self.workers.append(CrawlerThread(i, 'CrawlerThread' + str(i), self.frontier))

    def run(self):
        """The main Program"""
        try:
            for i in range(self.num_workers):
                self.workers[i].start()
            while True:
                self.frontier.distribute()
        except KeyboardInterrupt:
            self.frontier.save_to_crawl()
