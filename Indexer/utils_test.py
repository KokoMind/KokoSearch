from Indexer.utils import *

stemmer = Stemmer()
tokenizer = Tokenizer()

print(stemmer.stem("swimming"))
print(stemmer.stem("playing"))
print(stemmer.stem("work"))
print(stemmer.stem("fucked"))
print(stemmer.stem("tapping"))
print(stemmer.stem("died"))
print(stemmer.stem("sleep"))

print(tokenizer.tokenize("hello, world!"))
print(tokenizer.tokenize("hello my name is omar!"))
print(tokenizer.tokenize("fuck you :v"))
