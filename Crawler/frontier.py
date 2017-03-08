from . import prioritised_queue


class Frontier:
    """Class which will contain ToCrawl pages"""

    def __init__(self, num_threads):
        self.to_serve = []
        self.queues = [prioritised_queue] * num_threads
        self.attended_websites = [list] * num_threads

    def push_to_serve(self,element):
        self.to_serve.append(element)

    def pop_to_worker(self,thread_id):
        pass

    def save_to_crawl(self):
        pass

    def load_to_crawl(self):
        pass