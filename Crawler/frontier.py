from Crawler.prioritised_queue import PrioritisedQueue
from Crawler.storage import Storage
from queue import Queue


class Frontier:
    """Class which will contain ToCrawl pages"""

    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.to_serve = []
        self.queues, self.attended_websites = [], []
        for i in range(num_threads):
            self.queues.append(PrioritisedQueue())
            self.attended_websites.append({})
        self.turn = -1
        self.crawled = 0

    def push_to_serve(self, element):
        self.to_serve.extend(element)

    def distribute(self):
        # print("distributing")
        while len(self.to_serve):
            print("serving one link")
            url, dns, properties = self.to_serve.pop(0)
            value = Frontier._calc_priority(properties)
            if (not dns) or (Storage.cache_hash(url) == 1):
                continue
            for i in range(self.num_threads):
                if dns in self.attended_websites[i]:
                    print("found dns ----------------------------")
                    self.queues[i].push(value, url, dns)
                    break
            else:
                turn_ = self._get_turn()
                self.queues[turn_].push(value, url, dns)
                self.attended_websites[turn_][dns] = 1

    def get_url(self, thread_id):
        ret = self.queues[thread_id].pop()
        if not ret:
            return None, None, None
        else:
            self.crawled += 1
            return ret

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
        ret_code, links = Storage.get_to_crawl()
        turn_ = -1
        if ret_code == 0:  # successfull
            for value, url, dns in links:
                if (not dns) or (Storage.cache_hash(url) == 1):
                    continue
                for i in range(self.num_threads):
                    if dns in self.attended_websites[i]:
                        self.queues[i].push(value, url, dns)
                        break
                else:
                    turn_ += 1
                    turn_ %= self.num_threads
                    self.queues[turn_].push(value, url, dns)
                    self.attended_websites[turn_][dns] = 1
        else:
            print("Cannot Crawl")
        pass

    @staticmethod
    def _calc_priority(properties):
        """Properties (no.out_links, size_parent, size_url, parent_priority) constants of k1,k2,k3,k4 Equation = k1*A/sum + k2*B/sum + k3*C/sum + k4*D/sum"""
        k1, k2, k3, k4 = 0.3, 0.4, 0.2, 0.1
        A, B, C, D = properties[0], properties[1], properties[2], properties[3]
        summation = sum(properties)
        ret = k1 * A / summation + k2 * B / summation + k3 * (1 - (C / summation)) + k4 * D / summation
        return ret

    def _get_turn(self):
        if self.crawled < 1000:
            self.turn += 1
            self.turn %= self.num_threads
            return self.turn
        for i in range(self.num_threads):
            if self.queues[i].size == 0:
                self.turn = i
                return self.turn
        q_sz, dns_sz = [], []
        score = []
        for i in range(self.num_threads):
            q_sz.append(self.queues[i].size)
            dns_sz.append(len(self.attended_websites[i]))
            score.append(float(q_sz[i] * dns_sz[i]) / (0.5 * float(q_sz[i]) + 0.5 * float(dns_sz[i]) + 0.000000001))
        return score.index(min(score))


class FrontierRevisit:
    """Class which will contain ToCrawl pages in revisiting Process"""

    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.queues = []
        for i in range(num_threads):
            self.queues.append(Queue())
        self.turn = -1
        self.crawled = 0

    def get_url(self, thread_id):
        """Get the next url to revisit"""
        if self.queues[thread_id].empty():
            return None, None
        else:
            self.crawled += 1
            ret = self.queues[thread_id].get()
            return ret[0], ret[1]

    def distribute(self):
        # Get links from database
        ret, links = Storage.get_crawled()
        if ret == 0:
            print("distributing")
            for link in links:
                self.turn += 1
                self.turn %= self.num_threads
                self.queues[self.turn].put(link)
            print("Distribuing Finished")
        else:
            print("Error in distributing")
