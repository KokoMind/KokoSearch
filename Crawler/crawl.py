"""Main file to start crawling process"""

from Crawler.controller import Controller


class Config:
    num_threads = 5
    seeds = [('https://www.wikipedia.org/', '91.198.174.192'),
             ('https://www.stackoverflow.com', '	151.101.1.69'),
             ('https://www.quora.com', '54.210.178.68'),
             ]


def crawl():
    crawler = Controller(Config.num_threads, Config.seeds)
    crawler.run()


if __name__ == "__main__":
    crawl()
