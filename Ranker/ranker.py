import gensim
from query_processor import *
from pymongo import MongoClient
import operator


class Ranker:
    def __init__(self, _id2word_path, corpus_path, model_path):
        self._id2word_path = _id2word_path
        self._corpus_path = corpus_path
        self._construct_corpus()
        self.model_path = model_path
        self._load_model()
        self.query_processor = QueryProcessor()
        self.inverted_indexer_results_num = 50
        self.inverted_collections = []
        for i in range(16):
            db = MongoClient()['inverted_database_final_{0}'.format(i)]
            self.inverted_collections.append(db['inverted_indexer'])

    def _construct_corpus(self):
        self._id2word = gensim.corpora.Dictionary.load_from_text(self._id2word_path)
        self._corpus = gensim.corpora.MmCorpus(self._corpus_path)

    def _load_model(self):
        self._lda = gensim.models.LdaModel.load(self.model_path)

    def inverted_indexer_search(self, query):
        urls = []
        snapits = {}

        for i in range(16):
            if self.query_processor.is_qoute(query):
                results = self.inverted_collections[i].find({'$text': {'$search': query}})
                for j, record in enumerate(results):
                    urls.append(record['url'])
                    snapits[record['url']] = record['neighbours']
                    if j == self.inverted_indexer_results_num / 16:
                        break

            else:
                tokens = self.query_processor.process(query)
                score = {}
                for token in tokens:
                    batch = self.inverted_collections[i].find({'word': token})
                    for record in batch:
                        score[record['url']] += 1
                        snapits[record['url']] += record['neighbours']

                results = sorted(score.items(), key=operator.itemgetter(1))

                urls += [url for url, value in results.items()][:self.inverted_indexer_results_num / 16]

        return urls, snapits
