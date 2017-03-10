"""Main file to start crawling process"""

from Crawler.controller import Controller
from Crawler.fetcher import Fetcher


class Config:
    num_threads = 20
    seeds = [('https://en.wikipedia.org/', Fetcher.extract_dns('https://en.wikipedia.org/'), (0, 0, 10, 1)),
             ('https://www.quora.com/', Fetcher.extract_dns('https://www.quora.com/'), (0, 0, 10, 1)),
             ('https://www.reddit.com/', Fetcher.extract_dns('https://www.reddit.com/'), (0, 0, 10, 1)),
             ("http://www.dmoz.org/", Fetcher.extract_dns('https://www.reddit.com/'), (0, 0, 10, 1)),
             ]


def crawl():
    crawler = Controller(Config.num_threads, Config.seeds)
    crawler.run()


if __name__ == "__main__":
    crawl()
