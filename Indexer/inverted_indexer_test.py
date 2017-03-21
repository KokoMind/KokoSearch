from Indexer.inverted_indexer import *

threads = []

for i in range(4):
    threads.append(InvertedIndexer(i, 4))
    threads[i].start()  # This actually causes the thread to run
