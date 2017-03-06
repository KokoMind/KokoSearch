from peewee import *

import threading


class DBWorker(threading.Thread):
    """Class for a thread which will do a specific task in database"""

    def __init__(self, thread_id, name):
        """Construct a new db thread"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
