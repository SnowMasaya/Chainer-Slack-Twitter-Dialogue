#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from class_summary import ClassSummary
import random
import queue
import time
LIMIT_SIZE = 80000
global queue
queue = queue.Queue(LIMIT_SIZE)
from os import path
APP_ROOT = path.dirname(path.abspath( __file__ ))


class ProducerConsumerClassSummary(object):
    """
    Producer
    Consumer
    Multi Thread Class Summary.
    Using the Consumer Producer pattern
    Reference
        Python Consumer Producer pattern
            http://agiliq.com/blog/2013/10/producer-consumer-problem-in-python/
        Multi Thread Design pattern
    """
    def producer_run(self, file_list):
        """
        Running Producer
        Setting read word net file into the Queue
        """
        while True:
            for read_file in file_list:
                try:
                    print("Produced %s", read_file.strip())
                    queue.put(read_file.strip())
                    time.sleep(random.random())
                except ValueError:
                    continue

    def consumer_run(self, wiki_vector):
        """
        Running Consumer
        Taking the Calculate average vector
        """
        while True:
            try:
                read_file = queue.get()
                print("Consume %s", read_file)
                class_summary = ClassSummary(read_file, wiki_vector)
                class_summary.summary_class()
                queue.task_done()
                time.sleep(random.random())
            except queue.Empty:
                continue


