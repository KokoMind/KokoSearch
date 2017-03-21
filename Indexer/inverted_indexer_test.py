from Indexer.inverted_indexer import *
import timeit


def test():
    threads = []

    for i in range(4):
        threads.append(InvertedIndexer(i, 4))
        threads[i].start()  # This actually causes the thread to run

    for i in range(4):
        threads[i].join()


print(timeit.timeit(test()))
