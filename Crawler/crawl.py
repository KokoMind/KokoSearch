"""Main file to start crawling process"""

from Crawler.controller import Controller, ControllerRevisit
from Crawler.fetcher import Fetcher


class Config:
    """Class Config contain the configuration of the crawler and the seeds """
    crawling = True
    revisiting = False
    num_threads = 16
    cont_to_crawl = False
    seeds = ['https://en.wikipedia.org/',
             'https://www.quora.com/',
             'https://www.reddit.com/',
             "http://www.dmoz.org/",
             "https://www.amazon.com/",
             "http://www.ebay.com/",
             "https://en-maktoob.yahoo.com/",
             "http://www.W3.org/",
             "http://stanford.edu/",
             "https://www.cnet.com/",
             "http://www.berkeley.edu/",
             "https://www.spotify.com/",
             "http://www.springer.com/",
             "https://archive.org/",
             "http://www.ieee.org/",
             "http://www.nike.com/"
             ]


def make_seeds(Config):
    links = []
    for url in Config.seeds:
        links.append((url, Fetcher.extract_dns(url), (0, 0, 10, 1)))
    return links


def crawl():
    # Get the number of Crawler Threads
    Config.num_threads = int(input("Please Enter the Number of threads to crawl:"))
    seeds = make_seeds(Config)
    print("seeds are ready")
    crawler = Controller(Config.num_threads, seeds, Config.cont_to_crawl)
    crawler.run()


def revisit():
    # Get the number of Crawler Threads
    Config.num_threads = int(input("Please Enter the Number of threads to revisit:"))
    crawler = ControllerRevisit(Config.num_threads)
    crawler.run()


if __name__ == "__main__":
    if Config.crawling:
        crawl()
    elif Config.revisiting:
        revisit()
    else:
        print("Please Choose a proper mode.")
