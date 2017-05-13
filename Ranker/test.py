from ranker import Ranker

id2word_file = "./results/results_wordids.txt.bz2"
corpus = "./results/results_tfidf.mm"
model = "./lda_model/lda.model"
rank = Ranker(_id2word_path=id2word_file, corpus_path=corpus, model_path=model)

lis,_=rank.search("dogs")
print (lis[:20])