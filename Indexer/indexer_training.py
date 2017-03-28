from lda_indexer import Lda_Indexer



dic="/mnt/results/results_wordids.txt.bz2"
corpus="/mnt/results/results_tfidf.mm"
model="/mnt/lda/lda.model"

threads_num = int(input('threads num: '))
thread_id = int(input('thread_id: '))
indexer = Lda_Indexer(dic,corpus, load=model,threads_num=threads_num,thread_id=thread_id)
indexer.index()