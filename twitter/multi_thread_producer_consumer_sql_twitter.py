#!/usr/bin/env python
from __future__ import print_function
import sys
sys.path.append('.')
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyximport
pyximport.install()
from sqlite_twitter_summary_cython import SqliteTwitterSummaryCython
from split_data.input_file_cython import InputFileCython
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))
import random
import queue
import time
"""
You setting Queue size for memory
Reference:
    http://ja.pymotw.com/2/Queue/
"""
SEED_DOMAIN_LIST_SIZE = 300
queue = queue.Queue(SEED_DOMAIN_LIST_SIZE)


class ProducerConsumerThreadSqlTwitter(object):
    """
    Producer
    Consumer
    Multi Thread Crawling.
    Using the Consumer Producer pattern
    Reference
        Python Consumer Producer pattern
            http://agiliq.com/blog/2013/10/producer-consumer-problem-in-python/
        Multi Thread Design pattern
    """
    def get_file_data(self, file):
        """
        get file data
        :param file: summary word net data
        :return:
        """
        self.input_module = InputFileCython(file)
        self.input_module.input_special_format_file()
        return self.input_module.get_file_data()

    def producer_run(self):
        """
        Running Producer
        """
        file_list = self.get_file_data(APP_ROOT + '/../Data/wn_total_summary_51519_limit05_out_put_list.txt')
        class_word_vector = {}
        for file in file_list:
            if file.strip() not in class_word_vector:
                word_list = (list(map(lambda x:x.strip(), self.get_file_data(APP_ROOT + "/../Data/wn_total_summary_51519_limit05_out_put/" + file.strip()))))
                class_word_vector.update({file.strip().replace("_summary.txt", ""): word_list})
        global queue
        while True:
            try:
                queue.put(class_word_vector)
            except queue.Empty:
                print("Queue Full")
                pass
            else:
                log_text = "Produced "
                print(log_text)
                time.sleep(random.uniform(0.0, 0.5))

    def consumer_run(self):
        """
        Running Consumer
        """
        global queue
        while True:
            try:
                class_word_vector = queue.get()
            except queue.Empty:
                print("Queue Empty")
                pass
            else:
                log_text = "Consume "
                print(log_text)
                sqlite_twitter = SqliteTwitterSummaryCython(class_word_vector)
                sqlite_twitter.call_sql()
                queue.task_done()
                # Setting the wait time, I refered to the bellow link
                #  https://www.w3.org/Protocols/HTTP-NG/http-prob.html
                time.sleep(random.uniform(0.601, 0.602))
