from .Indexer.utils import *
import gensim


class QueryProcessor:
    def __init__(self, _id2word_path, corpus_path, model_path):
        self._stemmer = Stemmer()
        self._tokenizer = Tokenizer()
        self._detector = StopWordsDetector()

        self._id2word_path = _id2word_path
        self._corpus_path = corpus_path
        self._construct_corpus()
        self.model_path = model_path

    def _construct_corpus(self):
        self._id2word = gensim.corpora.Dictionary.load_from_text(self._id2word_path)
        self._corpus = gensim.corpora.MmCorpus(self._corpus_path)

    def _load_model(self, load):
        self._lda = gensim.models.LdaModel.load(self.model_path)

    def is_qoute(self, query):
        return query[0] == "\"" and query[-1] == "\""

    def process(self, query):
        tokens = self._tokenizer.tokenize(query.lower())
        stemmed = []
        for token in tokens:
            if not self._detector.is_stop_word(token):
                stemmed_token = self._stemmer.stem(token)
                if len(stemmed_token) > 2:
                    stemmed.append(stemmed_token)

        return stemmed

    def get_topic(self, query):
        query = query.split()
        new_query = self._id2word.doc2bow(query)
        sorted_probs = sorted(self._lda[new_query], key=lambda x: x[1])
        top_topics = [key for key, _ in sorted_probs[:2]]
        top_topics += [-1] * 5
        return top_topics[0]
