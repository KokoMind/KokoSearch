import string


class Stemmer:
    _prefixes = ['ing', 'es', 's', 'ed', 'er']

    def __init__(self):
        with open('./data/vocs.txt') as f:
            vocs = f.readlines()

        with open('./data/stemmed.txt') as f:
            stemmed = f.readlines()

        stem_vocs = [x.strip() for x in vocs]
        stem_output = [x.strip() for x in stemmed]

        self.stem_dictionary = {}
        for voc, stemmed_voc in zip(stem_vocs, stem_output):
            self.stem_dictionary[voc] = stemmed_voc

    def stem(self, word):
        if word in self.stem_dictionary:
            return self.stem_dictionary[word]

        if len(word) > 3:
            for prefix in self._prefixes:
                if word.find(prefix, len(word) - len(prefix) - 1) != -1:
                    word = word[:len(word) - len(prefix)]
                    if len(word) > 1 and word[-1] == word[-2]:
                        word = word[:len(word) - 1]
                    break
        return word


class Tokenizer:
    _translate_table = dict((ord(char), ord(' ')) for char in string.punctuation)

    def tokenize(self, s):
        s = s.translate(self._translate_table)
        return s.split()


class StopWordsDetector:
    """class for detecting the important words"""

    def __init__(self):
        with open('./data/stop_words.txt') as f:
            content = f.readlines()

        self._stop_words = [x.strip() for x in content]

    def is_stop_word(self, word):
        return (word in self._stop_words) or any(char.isdigit() for char in word)

    def remove_stop_words(self, lis):
        lis = lis.split()
        s = ""
        for i in lis:
            if not self.is_stop_word(i):
                s += i + " "
        return s


# def sentence_parser(page):
#     sents = nltk.sent_tokenize(page)
#     return sents


