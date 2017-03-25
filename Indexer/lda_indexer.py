from Indexer.inverted_indexer import  Indexer
from gensim.models.ldamulticore import  LdaMulticore
import gensim
import operator
import Crawler.db_model as c_db
import threading
class Lda_Indexer(Indexer):
    def __init__(self,_id2word_file,corpus_file,num_topics=500,load=None,train=False):
        super().__init__()
        self.num_topics=num_topics
        self._id2word_file=_id2word_file
        self._corpus_file=corpus_file
        self._construct_corpus()
        self._cnt=[]
        self.threads_num=4
        if load != None:
            self._load_model()
        if train:
            self._train_model()
        self.lda_collection = self.db['lda_indexer']


    def _get_next_page(self,id):
        """get next page from the crawler database"""
        try:
            page = c_db.Crawled.get(c_db.Crawled.id == self._cnt[id])
            self._cnt[id] += self.threads_num
            return page
        except c_db.Crawled.DoesNotExist:
            return -1

    def _construct_corpus(self):
        self._id2word = gensim.corpora.Dictionary.load_from_text(self._id2word_file)
        self._corpus = gensim.corpora.MmCorpus(self._corpus_file)

    def _train_model(self):
        self._lda = LdaMulticore(corpus=self._corpus, id2word=self._id2word, num_topics=self.num_topics, workers=1, chunksize=10000, passes=1)
        self._save_model()
    def _save_model(self):
        self._lda.save('lda.model')

    def _load_model(self):
        self._lda=gensim.models.LdaModel.load('lda.model')


    def _eval_doc(self,doc):
        doc=doc.split()
        new_doc=self._id2word.doc2bow(doc)
        sorted_probs=self._lda[new_doc].sort(key=operator.itemgetter(1))
        top_topics, _ = [list(c) for c in zip(*sorted_probs[:5])]
        new_list = [x + 1 for x in top_topics]
        return new_list


    def _add_document(self, url,c1,c2,c3,c4,c5):
        new_record={"url":url,"c1":c1,"c2":c2,"c3":c3,"c4":c4,"c5":c5}
        self.lda_collection.insert_one(new_record)



    def index(self,id):
        page = self._get_next_page(id)
        while page != -1:
            page_text = page.content
            page_url = page.url
            top_topics=self._eval_doc(page_text)
            doc_tuple = self._get_Document(page_url)
            self._add_document(page_url,top_topics[0],top_topics[1],top_topics[2],top_topics[3],top_topics[4])

            page = self._get_next_page(id)

    def index_all(self):
        for i in range(self.threads_num):
            self._cnt.append(i+1)
            t = threading.Thread(target=self.index, args=(i))
            t.daemon = True
            t.start()
