from Indexer.db_model import *
from Indexer.utils import *
import Crawler.db_model as c_db
import pymongo
from pymongo import MongoClient


class Indexer:
    def __init__(self):
        self._read_cnt = 1
        self._stemmer = Stemmer()
        self._tokenizer = Tokenizer()
        self._detector = StopWordsDetector()
        self.db = MongoClient()['indexer_database']

    def _get_next_page(self):
        """get next page from the crawler database"""
        try:
            page = c_db.Crawled.get(c_db.Crawled.id == self._read_cnt)
            self._read_cnt += 1
            return page
        except c_db.Crawled.DoesNotExist:
            return -1


class InvertedIndexer(Indexer):
    """the inverted indexer class"""

    def __init__(self):
        super().__init__()
        self.flushed_docs = 0
        self.flushed_word_doc = 0
        self.flushed_words = 0
        self.inverted_collection = self.db['inverted_indexer']

    def _insert_record(self, word, url, pos, neighbours):
        record = {"word": word,
                  "url": url,
                  "pos": pos,
                  "neighbours": neighbours}
        self.inverted_collection.insert_one(record)

    def index(self):
        """fill the inverted indexer database"""
        page = self._get_next_page()
        x = 0
        while page != -1:
            x += 1
            print(x)

            # process over doc
            page_text = page.content.lower()
            page_url = page.url

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
