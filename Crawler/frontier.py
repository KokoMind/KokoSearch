from Crawler.prioritised_queue import PrioritisedQueue


class Frontier:
    """Class which will contain ToCrawl pages"""

    def __init__(self, num_threads):
        self.to_serve = []
        self.queues = [PrioritisedQueue] * num_threads
        self.attended_websites = [list] * num_threads

    def push_to_serve(self, element):
        self.to_serve.append(element)

    def distribute(self, thread_id):
        pass

    def get_url(self, thread_id):
        return self.queues[thread_id].pop()[1]

    def save_to_crawl(self):
        pass

    def load_to_crawl(self):
        pass
