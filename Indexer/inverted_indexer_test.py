from inverted_indexer import *
import time

threads_num = 32


def test():
    threads = []

    for i in range(threads_num):
        threads.append(InvertedIndexer(i, threads_num))
        threads[i].start()  # This actually causes the thread to run

    for i in range(threads_num):
        threads[i].join()


start_time = time.time()

test()

print("--- %s seconds ---" % (time.time() - start_time))
