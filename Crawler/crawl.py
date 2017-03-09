"""Main file to start crawling process"""

from Crawler.controller import Controller
from Crawler.fetcher import Fetcher


class Config:
    num_threads = 5
    seeds = [('https://www.wikipedia.org/', Fetcher.extract_dns('https://www.wikipedia.org/')),
             ('https://www.quora.com/', Fetcher.extract_dns('https://www.quora.com/')),
             ('https://www.reddit.com/', Fetcher.extract_dns('https://www.reddit.com/')),
             ]


def crawl():
    crawler = Controller(Config.num_threads, Config.seeds)
    crawler.run()


if __name__ == "__main__":
    crawl()