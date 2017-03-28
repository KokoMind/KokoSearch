from lda_indexer import Lda_Indexer



path="/mnt/results/results_wordids.txt.bz2"
path2="/mnt/results/results_tfidf.mm"
indexer = Lda_Indexer(path,path2, train=True)
