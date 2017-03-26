from utils import *
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
        self._read_cnt = thread_id * 1000
        self._threads_num = threads_num
        self.db = MongoClient()['inverted_database_{0}'.format(thread_id)]
        self.inverted_collection = self.db['inverted_indexer']

    def _insert_record(self, word, url, pos, neighbours):
        record = {"word": word,
                  "url": url,
                  "pos": pos,
                  "neighbours": neighbours}
        self.inverted_collection.insert_one(record)

    def index(self):
        """fill the inverted indexer database"""

        batch = self.crawled.find({'my_id_1': {'$in': [x for x in range(self._read_cnt, self._read_cnt + 999)]}})

        while batch.count() > 0:
            self._read_cnt += 1000 * self._threads_num
            print(self._read_cnt)

            for page in batch:

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

            batch = self.crawled.find({'my_id_1': {'$in': [x for x in range(self._read_cnt, self._read_cnt + 999)]}})

    def run(self):
        self.index()
