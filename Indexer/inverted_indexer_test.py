from inverted_indexer import *
import time

# threads_num = 16


# def test():
#     threads = []
#
#     for i in range(threads_num):
#         threads.append(InvertedIndexer(i, threads_num))
#         threads[i].start()  # This actually causes the thread to run
#
#     for i in range(threads_num):
#         threads[i].join()

def test():
    threads_num = int(input('threads num: '))
    thread_id = int(input('thread_id: '))
    start_from = int(input('start from: '))
    indexer = InvertedIndexer(thread_id, threads_num, start_from)
    indexer.index()

test()