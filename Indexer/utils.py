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
