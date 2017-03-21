from Indexer.inverted_indexer import *
import time


def test():
    threads = []

    for i in range(4):
        threads.append(InvertedIndexer(i, 4))
        threads[i].start()  # This actually causes the thread to run

    for i in range(4):
        threads[i].join()


start_time = time.time()

test()

print("--- %s seconds ---" % (time.time() - start_time))
