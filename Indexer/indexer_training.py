from lda_indexer import Lda_Indexer



dic="./results/results_wordids.txt.bz2"
corpus="./results/results_tfidf.mm"
model="./lda_model/lda.model"

threads_num = int(input('threads num: '))
thread_id = int(input('thread_id: '))
print("ok")
indexer = Lda_Indexer(dic,corpus, load=model,threads_num=threads_num,thread_id=thread_id)
print("done")
indexer.index()