"""Main file to start crawling process"""

from Crawler.controller import Controller


class Config:
    num_threads = 5


def crawl():
    crawler = Controller(Config.num_threads)
    crawler.run()


if __name__ == "__main__":
    crawl()
