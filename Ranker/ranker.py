import gensim
from query_processor import QueryProcessor
from pymongo import MongoClient
import operator


class Ranker:
    def __init__(self, _id2word_path, corpus_path, model_path):
        self.query_processor = QueryProcessor(_id2word_path, corpus_path, model_path)
        self.inverted_indexer_results_num = 1000
        self.inverted_collections = []
        self.lda_collections = []
        for i in range(16):
            db = MongoClient()['inverted_database_final_{0}'.format(i)]
            self.inverted_collections.append(db['inverted_indexer'])

        for i in range(4):
            db = MongoClient()['lda_database_final_{0}'.format(i)]
            self.lda_collections.append(db['lda_indexer'])

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
                        if record['url'] in score:
                            score[record['url']] += 1
                            snapits[record['url']] += ' - ' + record['neighbours']
                        else:
                            score[record['url']] = 1
                            snapits[record['url']] = record['neighbours']

                results = sorted(score.items(), key=operator.itemgetter(1))

                urls += [url for (url, value) in results][:self.inverted_indexer_results_num / 16]

        return urls, snapits

    def search(self, query):
        print("start")
        query_topic = self.query_processor.get_topic(query)
        inverted_indexer_urls, snippets = self.inverted_indexer_search(query)
        same_topic = {}
        for url in inverted_indexer_urls:
            same_topic[url] = False
        for i in range(4):
            batch = self.lda_collections[i].find({"c1": query_topic, 'url': {'$in': inverted_indexer_urls}}, no_cursor_timeout=True)
            for record in batch:
                same_topic[record['url']] = True
        lis1 = []
        lis2 = []
        for url in inverted_indexer_urls:
            if same_topic[url]:
                lis1.append(url)
            else:
                lis2.append(url)

        return lis1 + lis2, snippets
