"""Main file to start crawling process"""

from controller import Controller, ControllerRevisit
from fetcher import Fetcher


class Config:
    """Class Config contain the configuration of the crawler and the seeds """
    crawling = True
    revisiting = False
    num_threads = 16
    cont_to_crawl = True
    seeds = ["https://en.wikipedia.org/",
             "http://www.W3.org/",
             "http://web.mit.edu/",
             "http://stanford.edu/",
             "https://www.rottentomatoes.com/",
             "http://www.imdb.com/",
             "http://screenrant.com/",
             "https://vimeo.com/",
             "http://www.100bestwebsites.org/",
             "http://www.makeuseof.com/tag/best-websites-internet/",
             "https://moz.com/top500",
             "https://www.bloomberg.com/",
             "https://www.reddit.com/r/Futurology/comments/48b5oc/best_of_2015_winners/",
             "https://moz.com/blog",
             "http://www.berkeley.edu/",
             "https://www.cam.ac.uk/",
             "http://www.ox.ac.uk/",
             "http://www.caltech.edu/",
             "http://www.dmoz.org/",
             "http://www.ebay.com/",
             "https://www.cnet.com/",
             "https://www.spotify.com/",
             "https://archive.org/",
             "http://www.ieee.org/",
             "http://www.nike.com/",
             "https://en-maktoob.yahoo.com/"
             ]


def make_seeds(Config):
    links = []
    for url in Config.seeds:
        links.append((url, Fetcher.extract_dns(url), (1000000, 1000000, 1, 1)))
    return links


def crawl():
    # Get the number of Crawler Threads
    Config.num_threads = int(input("Please Enter the Number of threads to crawl:"))
    # print("Wait for seeds to be ready")
    seeds = make_seeds(Config)
    # print("seeds are ready")
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
