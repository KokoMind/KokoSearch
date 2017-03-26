from Indexer.utils import *
import Crawler.db_model as c_db
from pymongo import MongoClient
import threading


class Indexer:
    def __init__(self, thread_id):
        super(Indexer, self).__init__()
        self._read_cnt = 1
        self._stemmer = Stemmer()
        self._tokenizer = Tokenizer()
        self._detector = StopWordsDetector()
        self.db = MongoClient()['indexer_database_{0}'.format(thread_id)]
        crawler_db = MongoClient()['crawled']
        self.crawled = crawler_db['crawled']


class InvertedIndexer(Indexer, threading.Thread):
    """the inverted indexer class"""

    def __init__(self, thread_id, threads_num):
        super().__init__(thread_id)
        self._read_cnt = thread_id + 1
        self._threads_num = threads_num
        self.inverted_collection = self.db['inverted_indexer']

    def _get_next_page(self):
        """get next page from the crawler database"""
        page = self.crawled.find({'my_id_1': self._read_cnt})

        if page.count() > 0:
            self._read_cnt += self._threads_num
            return page[0]

        else:
            return -1

    def _insert_record(self, word, url, pos, neighbours):
        record = {"word": word,
                  "url": url,
                  "pos": pos,
                  "neighbours": neighbours}
        self.inverted_collection.insert_one(record)

    def index(self):
        """fill the inverted indexer database"""
        page = self._get_next_page()

        while page != -1:
            print(self._read_cnt)

            # process over doc
            page_text = page['content'].lower()
            page_url = page['url']

            tokens = self._tokenizer.tokenize(page_text)
            for i, token in enumerate(tokens):
                if self._detector.is_stop_word(token):
                    continue

                stemmed = self._stemmer.stem(token)

                if len(stemmed) < 3:
                    continue

                neighbours = ''
                for j in range(max(0, i - 5), min(len(tokens), i + 5)):
                    neighbours += (tokens[j] + ' ')

                self._insert_record(stemmed, page_url, i, neighbours)

            page = self._get_next_page()

    def run(self):
        self.index()
