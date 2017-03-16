from queue import PriorityQueue


class PrioritisedQueue:
    def __init__(self):
        self.queue = PriorityQueue()

    def push(self, val, url, dns):
        self.queue.put((1 - val, url, dns))  # Minimum Priority Queue
        # print("new link pushed")

    def pop(self):
        if not self.queue.empty():
            return self.queue.get()
        else:
            return None

    def queue_to_list(self):
        return list(self.queue.queue)

    @property
    def size(self):
        return self.queue.qsize()
