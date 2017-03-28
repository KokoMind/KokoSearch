from inverted_indexer import  Indexer
from gensim.models.ldamulticore import  LdaMulticore
import gensim
import operator
import threading
import logging
import time

from pymongo import MongoClient

class Lda_Indexer(Indexer):
    def __init__(self,_id2word_file,corpus_file,threads_num,thread_id,num_topics=500,load=None,train=False):
        super().__init__()
        self.num_topics=num_topics
        self._id2word_file=_id2word_file
        self._corpus_file=corpus_file
        self._construct_corpus()
        self.threads_num=threads_num
        self._read_cnt =  thread_id * 1000
        self._to_be_inserted = []
        db = MongoClient()['inverted_database_final_{0}'.format(thread_id)]
        self.lda_collection = self.db['lda_indexer']




        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        if load != None:
            self._load_model(load)
        if train:
            self._train_model()

    def _construct_corpus(self):
        self._id2word = gensim.corpora.Dictionary.load_from_text(self._id2word_file)
        self._corpus = gensim.corpora.MmCorpus(self._corpus_file)

    def _train_model(self):
        self._lda = LdaMulticore(corpus=self._corpus, id2word=self._id2word, num_topics=self.num_topics, workers=1, chunksize=10000, passes=1)
        self._save_model()
    def _save_model(self):
        self._lda.save('lda.model')

    def _load_model(self,load):
        self._lda=gensim.models.LdaModel.load(load)


    def _eval_doc(self,doc):
        doc=doc.split()
        new_doc=self._id2word.doc2bow(doc)
        sorted_probs=sorted(self._lda[new_doc],key=lambda x: x[1])
        top_topics, _ = [list(c) for c in zip(*sorted_probs[:5])]
        top_topics+=[-1]*5
        return top_topics[:5]


    def _add_document(self, url,c1,c2,c3,c4,c5):
        new_record={"url":url,"c1":c1,"c2":c2,"c3":c3,"c4":c4,"c5":c5}
        self._to_be_inserted.append(new_record)
        if len(self._to_be_inserted) > 1000:
            self.lda_collection.insert_many(self._to_be_inserted)
            self._to_be_inserted = []




    def index(self):
        batch = self.crawled.find({'my_id_1': {'$in': [x for x in range(self._read_cnt, self._read_cnt + 999)]}}, no_cursor_timeout=True)

        while batch.count() > 0:
            start_time = time.time()
            for page in batch:
                page_text =  page['content'].lower()
                page_url = page['url']
                top_topics=self._eval_doc(page_text)
                self._add_document(page_url,top_topics[0],top_topics[1],top_topics[2],top_topics[3],top_topics[4])

            batch.close()
            batch = self.crawled.find({'my_id_1': {'$in': [x for x in range(self._read_cnt, self._read_cnt + 999)]}}, no_cursor_timeout=True)

            print("--- %s seconds ---" % (time.time() - start_time))

