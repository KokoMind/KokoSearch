from .inverted_indexer import  Indexer
from gensim.models.ldamulticore import  LdaMulticore
import gensim
import operator

class Lda_Indexer(Indexer):
    def __init__(self):
        super.__init__()


    def construct_corpus(self,_id2word_file,corpus_file):
        self._id2word = gensim.corpora.Dictionary.load_from_text(_id2word_file)
        self._corpus = gensim.corpora.MmCorpus(corpus_file)

    def train_model(self,num_topics):
        self._lda = LdaMulticore(corpus=self._corpus, id2word=self.id2word, num_topics=num_topics, update_every=1, chunksize=10000, passes=1)

    def save_model(self):
        self._lda.save('lda.model')


    def eval_doc(self,doc):
        new_doc=self._id2word.doc2bow(doc)
        sorted_probs=self._lda[new_doc].sort(key=operator.itemgetter(1))
        top_topics, b = [list(c) for c in zip(*sorted_probs[:5])]
        new_list = [x + 1 for x in top_topics]

        return new_list


    