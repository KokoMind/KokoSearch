import string
import nltk


class Stemmer:
    _prefixes = ['ing', 'es', 's', 'ed', 'er']

    def stem(self, word):
        if len(word) > 3:
            for prefix in self._prefixes:
                if word.find(prefix, len(word) - len(prefix) - 1) != -1:
                    word = word[:len(word) - len(prefix)]
                    if word[-1] == word[-2]:
                        word = word[:len(word) - 1]
        return word


class Tokenizer:
    _translate_table = dict((ord(char), ord(' ')) for char in string.punctuation)

    def tokenize(self, s):
        s = s.translate(self._translate_table)
        return s.split()


class StopWordsDetector:
    """class for detecting the important words"""

    def __init__(self):
        with open('stop_words.txt') as f:
            content = f.readlines()

        self._stop_words = [x.strip() for x in content]

    def is_stop_word(self, word):
        return word in self._stop_words

    def remove_stop_words(self,lis):
        new_lis=[]
        for i in lis:
            if not self.is_stop_word(i):
                new_lis.append(i)
        return new_lis

def sentence_parser(page):
    sents = nltk.sent_tokenize(page)
    return sents