import gensim
from Ranker.query_processor import QueryProcessor
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
        score = {}

        for i in range(16):
            if self.query_processor.is_qoute(query):
                db_results = self.inverted_collections[i].find({'$text': {'$search': query}}, no_cursor_timeout=True).limit(100)
                for j, record in enumerate(db_results):
                    urls.append((record['url'], record['neighbours']))
                    if j == self.inverted_indexer_results_num / 16:
                        break
                db_results.close()

            else:
                tokens = self.query_processor.process(query)

                for token in tokens:
                    batch = self.inverted_collections[i].find({'word': token}, no_cursor_timeout=True).limit(300)
                    for record in batch:
                        if record['url'] in score:
                            score[record['url']] += 1
                            snapits[record['url']] += ', ' + record['neighbours']
                        else:
                            score[record['url']] = 1
                            snapits[record['url']] = record['neighbours']
                    batch.close()

        if not self.query_processor.is_qoute(query):
            results = sorted(score.items(), key=operator.itemgetter(1), reverse=True)

            urls = [(url, snapits[url][:350]) for (url, value) in results][:int(self.inverted_indexer_results_num / 16)]

        return urls

    def search(self, query):
        print("start")
        query_topic = self.query_processor.get_topic(query)
        inverted_indexer_urls = self.inverted_indexer_search(query)
        same_topic = {}
        urls=[]
        for url,snippet in inverted_indexer_urls:
            same_topic[url] = False
            urls.append(url)
        for i in range(4):
            print(i)
            batch = self.lda_collections[i].find({"c1": query_topic, 'url': {'$in': urls}}, no_cursor_timeout=True)
            for record in batch:
                same_topic[record['url']] = True
        lis1 = []
        lis2 = []
        for url,snippet in inverted_indexer_urls:
            if same_topic[url]:
                lis1.append((url,snippet))
            else:
                lis2.append((url,snippet))

        return lis1 + lis2
