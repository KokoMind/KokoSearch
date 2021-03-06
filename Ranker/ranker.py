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
        hosts = []

        for i in range(1):
            print("\nFML", i)
            if self.query_processor.is_qoute(query):
                clean_query = query[1:-1]
            else:
                clean_query = query

            tokens = self.query_processor.process(clean_query)

            for token in tokens:
                showed = []
                print("\ntoken ", token)
                batch = self.inverted_collections[i].find({'word': token}, no_cursor_timeout=True).limit(4000)
                for record in batch:
                    print('.', end="")
                    if not self.query_processor.is_qoute(query) or self.query_processor.is_qoute(query) and clean_query in record['neighbours']:
                        if record['url'] in score:
                            if record['url'] in showed:
                                score[record['url']] += 1
                            else:
                                score[record['url']] += 100
                                showed.append(record['url'])

                            snapits[record['url']] += ', ' + record['neighbours']
                        else:
                            if record['url'].split('/')[2] not in hosts:
                                hosts.append(record['url'].split('/')[2])
                                showed.append(record['url'])
                                score[record['url']] = 100
                                snapits[record['url']] = record['neighbours']
                batch.close()

        print('\nbegin sort')
        results = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
        print('finished sort')
        urls = [(url, snapits[url][:350]) for (url, value) in results][:int(self.inverted_indexer_results_num)]

        return urls

    def search(self, query):
        print("start")
        query_topic = self.query_processor.get_topic(query)
        inverted_indexer_urls = self.inverted_indexer_search(query)
        same_topic = {}
        urls = []
        for url, snippet in inverted_indexer_urls:
            same_topic[url] = False
            urls.append(url)
        for i in range(4):
            print(i)
            batch = self.lda_collections[i].find({"c1": query_topic, 'url': {'$in': urls}}, no_cursor_timeout=True)
            for record in batch:
                same_topic[record['url']] = True
        lis1 = []
        lis2 = []
        for url, snippet in inverted_indexer_urls:
            if same_topic[url]:
                lis1.append((url, snippet))
            else:
                lis2.append((url, snippet))

        return inverted_indexer_urls
