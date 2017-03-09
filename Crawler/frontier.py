from Crawler.prioritised_queue import PrioritisedQueue
from Crawler.storage import Storage


class Frontier:
    """Class which will contain ToCrawl pages"""

    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.to_serve = []
        self.queues = [PrioritisedQueue()] * num_threads
        self.attended_websites = [{}] * num_threads
        self.turn = 0

    def push_to_serve(self, element):
        self.to_serve.extend(element)

    def distribute(self):
        # print("distributing")
        while len(self.to_serve):
            print("serving one link")
            url, dns = self.to_serve.pop(0)
            if not dns or Storage.cache_hash(url) == 1:
                continue
            for i in range(self.num_threads):
                if dns in self.attended_websites[i]:
                    self.queues[i].push(0, url, dns)
                    break
            else:
                self.queues[self.turn].push(0, url, dns)
                self.attended_websites[self.turn][dns] = 1
                self.turn += 1
                self.turn %= self.num_threads

    def get_url(self, thread_id):
        ret = self.queues[thread_id].pop()
        if not ret:
            return None
        else:
            return ret[1]

    def save_to_crawl(self):
        arg = []
        for i in range(self.num_threads):
            arg.extend(self.queues[i].queue_to_list())
        if len(arg) == 0:
            return
        ret = Storage.cache_to_crawl(arg)
        if ret == 0:  # successful
            print("To_Crawl links are successfully cached")
        else:
            print("Error. Links 'To_crawl' are lost!")

    def load_to_crawl(self):
        pass
