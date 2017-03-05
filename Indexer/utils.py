import string


class Stemmer:
    prefixes = ['ing', 'es', 's', 'ed', 'er']

    def stem(self, word):
        for prefix in self.prefixes:
            if word.find(prefix, len(word) - len(prefix) - 1) != -1:
                word = word[:len(word) - len(prefix)]
                if word[-1] == word[-2]:
                    word = word[:len(word) - 1]
        return word


class Tokenizer:
    translate_table = dict((ord(char), ord(' ')) for char in string.punctuation)

    def tokenize(self, s):
        s = s.translate(self.translate_table)
        return s.split()


class StopWordsDetector:
    """class for detecting the important words"""

    def __init__(self):
        with open('stop_words.txt') as f:
            content = f.readlines()

        self.stop_words = [x.strip() for x in content]

    def is_stop_word(self, word):
        return word in self.stop_words