from Indexer.utils import *
from gensim import corpora, models
from gensim.models.ldamulticore import  LdaMulticore
import operator

id2word = corpora.Dictionary.load_from_text('/home/gemy/work/MachineLearning/my-projects/KokoSearch/Indexer/lda_model/trained_lda.model.id2word')
lda=models.LdaModel.load('/home/gemy/work/MachineLearning/my-projects/KokoSearch/Indexer/lda_model/trained_lda.model')
new_doc=id2word.doc2bow("i'm playing football")
sorted_probs=lda[new_doc].sort(key=operator.itemgetter(1))
top_topics, _ = [list(c) for c in zip(*sorted_probs[:5])]



