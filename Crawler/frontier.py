from prioritised_queue import PrioritisedQueue
from storage import Storage
from queue import Queue


class Frontier:
    """Class which will contain ToCrawl pages"""

    def __init__(self, num_threads, dash_):
        self.num_threads = num_threads
        self.dash = dash_
        self.to_serve, self.queues, self.attended_websites, self.threads_tracking = [], [], [], []
        for i in range(num_threads):
            self.to_serve.append(Queue())
            self.queues.append(PrioritisedQueue())
            self.attended_websites.append({})
            self.threads_tracking.append({})
            self.threads_tracking[i]['tocrawl'] = 0
            self.threads_tracking[i]['dns'] = 0
        self.turn = -1
        self.crawled = 0

    def push_to_serve(self, element, thread_id):
        # [self.to_serve[thread_id].put(ele) for ele in element]
        for ele in element:
            self.to_serve[thread_id].put(ele)

    def pop_to_distribute(self):
        i = -1
        empty_i = 0
        while i < self.num_threads:
            i += 1
            i %= self.num_threads
            if not self.to_serve[i].empty():
                # print("got link")
                empty_i = 0
                yield self.to_serve[i].get()
            else:
                # print("empty")
                empty_i += 1
                pass
            if empty_i == self.num_threads:
                break

    def distribute(self):
        # print("distributing")
        for link in self.pop_to_distribute():
            # print("serving one link")
            url, dns, properties = link
            value = Frontier._calc_priority(properties)
            try:
                hashing = Storage.cache_hash(url)
            except:
                hashing = 0
            if (not dns) or (hashing == 1 or hashing == -1):
                continue
            for i in range(self.num_threads):
                if dns in self.attended_websites[i]:
                    self.queues[i].push(value, url, dns)
                    self.dash.print_tocrawl(str(self.queues[i].size), i)
                    break
            else:
                turn_ = self._get_turn()
                self.queues[turn_].push(value, url, dns)
                self.attended_websites[turn_][dns] = 1
                self.dash.print_tocrawl(str(self.queues[turn_].size), turn_)
                self.dash.print_dns(str(len(self.attended_websites[turn_])), turn_)

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
        ret = Storage.delete_to_crawl()
        if ret == 0:  # successful
            self.dash.print_frontier_stat("To_Crawl links are deleted success")
        else:
            self.dash.print_frontier_stat("Error. Cannot delete TO_crawl links")
        ret = Storage.cache_to_crawl(arg)
        if ret == 0:  # successful
            self.dash.print_frontier_stat("To_Crawl links are successfully cached")
        else:
            self.dash.print_frontier_stat("Error. Links 'To_crawl' are lost!")

    def load_to_crawl(self):
        ret_code, links = Storage.get_to_crawl()
        turn_ = -1
        if ret_code == 0:  # successfull
            for value, url, dns in links:
                for i in range(self.num_threads):
                    if dns in self.attended_websites[i]:
                        self.queues[i].push(value, url, dns)
                        break
                else:
                    turn_ += 1
                    turn_ %= self.num_threads
                    self.queues[turn_].push(value, url, dns)
                    self.attended_websites[turn_][dns] = 1
            for i in range(self.num_threads):
                self.dash.print_tocrawl(str(self.queues[i].size), i)
                self.dash.print_dns(str(len(self.attended_websites[i])), i)
            # print("Links loaded and distributed successfully")
            ret = Storage.delete_to_crawl()
            if ret == 0:  # successful
                self.dash.print_frontier_stat("To_Crawl links are deleted success")
            else:
                self.dash.print_frontier_stat("Error. Cannot delete TO_crawl links")
                # print("Table To crawl cleared successfully")
        else:
            self.dash.print_frontier_stat("Cannot Crawl")
        pass

    @staticmethod
    def _calc_priority(properties):
        """Properties (no.out_links, size_parent, size_url, parent_priority) constants of k1,k2,k3,k4 Equation = k1*A/sum + k2*B/sum + k3*C/sum + k4*D/sum"""
        k1, k2, k3, k4 = 0.4, 0.4, 0.1, 0.1
        A, B, C, D = properties[0], properties[1], properties[2], properties[3]
        summation = sum(properties)
        ret = k1 * A / summation + k2 * B / summation + k3 * (1 - (C / summation)) + k4 * (1 - D) / summation
        return ret

    def _get_turn(self):
        if len(self.attended_websites[0]) < 100:
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
