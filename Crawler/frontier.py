from Crawler.prioritised_queue import PrioritisedQueue
from Crawler.storage import Storage


class Frontier:
    """Class which will contain ToCrawl pages"""

    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.to_serve = []
        self.queues = [PrioritisedQueue()] * num_threads
        self.attended_websites = [{}] * num_threads

    def push_to_serve(self, element):
        self.to_serve.extend(element)

    def distribute(self):
        # print("distributing")
        while len(self.to_serve):
            print("serving one link")
            url, dns, properties = self.to_serve.pop(0)
            value = self._calc_priority(properties)
            if not dns or Storage.cache_hash(url) == 1:
                continue
            for i in range(self.num_threads):
                if dns in self.attended_websites[i]:
                    self.queues[i].push(value, url, dns)
                    break
            else:
                turn_ = self._get_turn()
                self.queues[turn_].push(value, url, dns)
                self.attended_websites[turn_][dns] = 1

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

    @staticmethod
    def _calc_priority(self, properties):
        """Properties (no.out_links, size_parent, size_url, parent_priority) constants of k1,k2,k3,k4 Equation = k1*A/sum + k2*B/sum + k3*C/sum + k4*D/sum"""
        k1, k2, k3, k4 = 0.25, 0.25, 0.4, 0.1
        A, B, C, D = properties[0], properties[1], properties[2], properties[3]
        summation = sum(properties)
        ret = k1 * A / summation + k2 * B / summation + k3 * C / summation + k4 * D / summation
        return ret

    def _get_turn(self):
        ret = 0
        q_sz, dns_sz = [], []
        score = []
        for i in range(self.num_threads):
            q_sz.append(self.queues[i].size)
            dns_sz.append(len(self.attended_websites[i]))
            score.append(float(q_sz[i] * dns_sz[i]) / (0.7 * float(q_sz) + 0.3 * float(dns_sz)))
        return score.index(min(score))
