from utils import *


class QueryProcessor:
    def __init__(self):
        self._stemmer = Stemmer()
        self._tokenizer = Tokenizer()
        self._detector = StopWordsDetector()

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
