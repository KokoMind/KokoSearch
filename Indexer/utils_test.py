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

tokens = tokenizer.tokenize(s)

sen=sentence_parser(
"""There is a new gensim feature to automatically choose the best model without a manual visualisation in pyLDAvis or word coloring. It is called ‘topic coherence’.  One of the students currently enrolled in our Incubator program, Devashish, has implemented this in Python based on paper by Michael Röder et al.
There is an interesting twist here. Surprisingly, a mathematically rigorous calculation of model fit (data likelihood, perplexity) doesn't always agree with human opinion about the quality of the model, as shown in a well-titled paper "Reading Tea Leaves: How Humans Interpret Topic Models". But another formula has been found to correlate well with human judgement. It is called 'C_v topic coherence'. It measures how often the topic words appear together in the corpus. Of course, the trick is how to define ‘together’. Gensim supports several topic coherence measures including C_v. You can explore them in this Jupyter notebook.
As expected from our manual inspections above, the model which trained for 50 epochs has higher coherence. Now you can automatically choose the best model using this number.
Conclusion
We have covered three ways to evaluate a topic model – coloring words, pyLDAvis and topic coherence. The one you choose depends on the number of models and topics. If you have a handful of models and a small number of topics, then you could run the manual inspections in a reasonable amount of time. Coloring swing words in your specific domain is an important one to get right. In other situations manual inspections are not feasible. For example, if you’ve run an LDA parameter grid search and have a lot of models, or if you have thousands of topics. In that case the only way is the automated topic coherence to find the most coherent model, then a quick manual validation of the winner with word coloring and pyLDAvis.
I hope you find these model selection techniques useful in your NLP applications! Let us know if you have any questions about them on the gensim mailing list. We also offer NLP consulting services at RaRe Technologies.
Lev KDN.jpgBio: Lev Konstantinovskiy, an expert in natural language processing, is a Python and Java developer. Lev has extensive experience working with financial institutions and is RaRe’s manager of open source communities including gensim, an open source machine learning toolkit for understanding human language. Lev holds the position of Open Source Evangelist, R&D at RaRe Technologies.""")
# print (len(sen))  #26
a=[]
for i in sen :
    a.append(tokenizer.tokenize(i)
   ) # print (detector.remove_stop_words(a))


id2word = corpora.Dictionary(a )
print(id2word)