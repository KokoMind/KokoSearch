from Indexer.utils import *
from gensim import corpora, models

stemmer = Stemmer()
tokenizer = Tokenizer()
detector = StopWordsDetector()

print(stemmer.stem("swimming"))
print(stemmer.stem("playing"))
print(stemmer.stem("work"))
print(stemmer.stem("fucked"))
print(stemmer.stem("tapping"))
print(stemmer.stem("died"))
print(stemmer.stem("sleep"))
print('')

print(tokenizer.tokenize("hello, world!"))
print(tokenizer.tokenize("hello my name is omar!"))
print(tokenizer.tokenize("fuck you :v"))

sentences = ['my name is omar and fuck you',
             'go fuck yourself please',
             'life is hard my friend']

for s in sentences:
    tokens = tokenizer.tokenize(s)
    print('')
    for token in tokens:
        if not detector.is_stop_word(token):
            print(token, end=" ")

print("")
