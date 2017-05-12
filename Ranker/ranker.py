import  gensim


class Ranker():
    def __init__(self, _id2word_path, corpus_path,model_path):
        self._id2word_path = _id2word_path
        self._corpus_path = corpus_path
        self._construct_corpus()
        self.model_path = model_path
        self._load_model()
    def _construct_corpus(self):
        self._id2word = gensim.corpora.Dictionary.load_from_text(self._id2word_path)
        self._corpus = gensim.corpora.MmCorpus(self._corpus_path)

    def _load_model(self):
        self._lda = gensim.models.LdaModel.load(self.model_path)

    def search(self):
        pass