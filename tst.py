from Ranker.ranker import Ranker



id2word_file = "./Ranker/results/results_wordids.txt.bz2"
corpus = "./Ranker/results/results_tfidf.mm"
model = "./Ranker/lda_model/lda.model"
rank = Ranker(_id2word_path=id2word_file, corpus_path=corpus, model_path=model)

lis = rank.search(input('enter your query: '))
print(lis[:20])


