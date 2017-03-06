from Indexer.utils import *
from gensim import corpora, models
from gensim.models.ldamulticore import  LdaMulticore

stemmer = Stemmer()
tokenizer = Tokenizer()
detector = StopWordsDetector()
txt = open('./meta_data/test.txt')
txt=txt.read()
sen=sentence_parser(txt)
a=[]
for i in sen :
    a.append(tokenizer.tokenize(i) ) # print (detector.remove_stop_words(a))


id2word = corpora.Dictionary( a )
corpus = [id2word.doc2bow(text) for text in a]
lda=LdaMulticore(corpus=corpus, id2word=id2word, num_topics=2,  chunksize=10000, passes=1)

