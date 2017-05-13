from Ranker.utils import *

# from gensim import corpora, models

stemmer = Stemmer()
tokenizer = Tokenizer()
detector = StopWordsDetector()

print(stemmer.stem("swimming"))
print(stemmer.stem("playing"))
print(stemmer.stem("work"))
print(stemmer.stem("loved"))
print(stemmer.stem("tapping"))
print(stemmer.stem("died"))
print(stemmer.stem("sleep"))
print(stemmer.stem("computers"))
print('')

print(tokenizer.tokenize("hello, world!"))
print(tokenizer.tokenize("hello my name is omar!"))
print(tokenizer.tokenize("love you :v"))

sentences = ['my name is omar and love you',
             'go love yourself please',
             'life is hard my friend']

for s in sentences:
    tokens = tokenizer.tokenize(s)
    print('')
    for token in tokens:
        if not detector.is_stop_word(token):
            print(token, end=" ")

print("")
