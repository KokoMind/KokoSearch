from queue import Queue


class PrioritisedQueue:
    def __init__(self):
        self.queue = Queue()

    def push(self, val, url, dns):
        self.queue.put((val, url, dns))
        print("new link pushed")

    def pop(self):
        if not self.queue.empty():
            return self.queue.get()
        else:
            return None

    def queue_to_list(self):
        return list(self.queue.queue)
