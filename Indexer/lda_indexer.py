from .inverted_indexer import  Indexer
from gensim.models.ldamulticore import  LdaMulticore
import gensim
import operator
from Indexer.db_model import *
from Indexer.utils import *
class Lda_Indexer(Indexer):
    def __init__(self,_id2word_file,corpus_file,num_topics=500,load=None):
        super.__init__()
        self.num_topics=num_topics
        self._id2word_file=_id2word_file
        self._id2word_file=corpus_file
        self._construct_corpus()
        if load != None:
            gensim.models.ldamodel.LdaModel.load(load)
    def fill_topics(self):
        #to be continued (add num of docs)
        for i in range(self.num_topics):
            Topic.create()


    def _construct_corpus(self):
        self._id2word = gensim.corpora.Dictionary.load_from_text(self._id2word_file)
        self._corpus = gensim.corpora.MmCorpus(self.corpus_file)

    def _train_model(self):
        self._lda = LdaMulticore(corpus=self._corpus, id2word=self.id2word, num_topics=self.num_topics, chunksize=10000, passes=1)
        self._save_model()

    def _save_model(self):
        self._lda.save('lda.model')

    def _eval_doc(self,doc):
        doc=doc.split()
        new_doc=self._id2word.doc2bow(doc)
        sorted_probs=self._lda[new_doc].sort(key=operator.itemgetter(1))
        top_topics, _ = [list(c) for c in zip(*sorted_probs[:5])]
        new_list = [x + 1 for x in top_topics]
        return new_list


    def _add_document(self, url,c1,c2,c3,c4,c5):
        return Document.create(url=url, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5)

    def _update_document(self, doc,c1,c2,c3,c4,c5):
        doc.c1,doc.c2,doc.c3,doc.c4,doc.c5=c1,c2,c3,c4,c5
        doc.save()

    def index(self):
        page = self._get_next_page()
        while page != -1:
            page_text = page.content
            page_url = page.url
            top_topics=self._eval_doc(page_text)
            with db.atomic():
                doc_tuple = self._get_Document(page_url)
                if doc_tuple == -1:
                    doc_tuple = self._add_document(page_url,top_topics[0],top_topics[1],top_topics[2],top_topics[3],top_topics[4])
                else :
                    self._update_document(top_topics[0],top_topics[1],top_topics[2],top_topics[3],top_topics[4])
            page = self._get_next_page()

