from Crawler.prioritised_queue import PrioritisedQueue
from Crawler.storage import Storage


class Frontier:
    """Class which will contain ToCrawl pages"""

    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.to_serve = []
        self.queues = [PrioritisedQueue] * num_threads
        self.attended_websites = [list] * num_threads

    def push_to_serve(self, element):
        self.to_serve.extend(element)

    def distribute(self, thread_id):
        pass

    def get_url(self, thread_id):
        return self.queues[thread_id].pop()[1]

    def save_to_crawl(self):
        arg = []
        for i in range(self.num_threads):
            arg.append(self.queues[i].queue_to_list())
        ret = Storage.cache_to_crawl()
        if ret == 0:  # successful
            print("To_Crawl links are successfully cached")
        else:
            print("Error. Links 'To_crawl' are lost!")

    def load_to_crawl(self):
        pass
