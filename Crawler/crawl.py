"""Main file to start crawling process"""

from Crawler.controller import Controller
from Crawler.fetcher import Fetcher


class Config:
    num_threads = 5
    seeds = [('https://en.wikipedia.org/', Fetcher.extract_dns('https://en.wikipedia.org/'), (0, 0, 0, 1)),
             ('https://www.quora.com/', Fetcher.extract_dns('https://www.quora.com/'), (0, 0, 0, 1)),
             ('https://www.reddit.com/', Fetcher.extract_dns('https://www.reddit.com/'), (0, 0, 0, 1)),
             ]


def crawl():
    crawler = Controller(Config.num_threads, Config.seeds)
    crawler.run()


if __name__ == "__main__":
    crawl()

print(Fetcher.fetch('https://www.wikipedia.org/'))
