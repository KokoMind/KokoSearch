from Indexer.utils import *
from gensim import corpora, models
stemmer = Stemmer()
tokenizer = Tokenizer()
detector = StopWordsDetector()

print(stemmer.stem("swimming"))
print(stemmer.stem("playing"))
print(stemmer.stem("work"))
print(stemmer.stem("tapping"))
print('')
print(tokenizer.tokenize("hello, world!"))



