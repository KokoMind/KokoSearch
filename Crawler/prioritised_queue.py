class prioritisedQueue:
    def __init__(self):
        self.queue = []

    def push(self, element):
        self.queue.append(element)

    def pop(self, element):
        if len(self.queue) > 0:
             self.queue.pop(0)
             return True
        return False
