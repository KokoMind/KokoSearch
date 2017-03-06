from Indexer.db_model import *
from Indexer.utils import *
import Crawler.db_model as c_db


class Indexer:
    def __init__(self):
        create_data_base()
        self._read_cnt = 1
        self._stemmer = Stemmer()
        self._tokenizer = Tokenizer()
        self._detector = StopWordsDetector()

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

    def _get_word(self, word):
        """get word from the inverted indexer database"""
        try:
            word = Word.get(Word.word == word)
            return word
        except Word.DoesNotExist:
            return -1

    def _get_Document(self, url):
        """get word from the inverted indexer database"""
        try:
            doc = Document.get(Document.url == url)
            return doc
        except Document.DoesNotExist:
            return -1

    def _add_word(self, word):
        """add word to the inverted indexer database"""
        return Word.create(word=word, num_of_docs=0)

    def _add_document(self, url):
        """add document to the inverted indexer database"""
        return Document.create(url=url, c1=0, c2=0, c3=0, c4=0, c5=0)

    def _add_connection(self, word_id, doc_id, pos, neighbours):
        """add connection between document and word"""
        return Word_Doc.create(doc_id=doc_id, word_id=word_id, pos=pos, neighbours=neighbours)

    def index(self):
        """fill the inverted indexer database"""
        page = self._get_next_page()
        while page != -1:
            # process over doc
            page_text = page.content
            page_url = page.url

            with db.atomic():
                doc_tuple = self._get_Document(page_url)
                if doc_tuple == -1:
                    doc_tuple = self._add_document(page_url)

            tokens = self._tokenizer.tokenize(page_text)
            for i, token in enumerate(tokens):
                if len(token) < 3 or self._detector.is_stop_word(token):
                    continue
                else:
                    stemmed = self._stemmer.stem(token)
                    word_tuple = self._get_word(stemmed)
                    if word_tuple == -1:
                        word_tuple = self._add_word(stemmed)

                    word_tuple.num_of_docs += 1
                    word_tuple.save()

                    neighbours = ''
                    for j in range(max(0, i - 5), min(len(tokens), i + 5)):
                        neighbours += (tokens[j] + ' ')

                    self._add_connection(word_tuple.id, doc_tuple.id, i, neighbours)

            page = self._get_next_page()
