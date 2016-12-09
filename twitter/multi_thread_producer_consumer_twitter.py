#!/usr/bin/env python
from __future__ import print_function
import sys
sys.path.append('.')
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from twitter_get_usr_timeline_module import TwitterGetUserTimelineModule
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
twiteet_queue = queue.Queue(SEED_DOMAIN_LIST_SIZE)
check_queue = queue.Queue(SEED_DOMAIN_LIST_SIZE)

class ProducerConsumerThreadTwitter(object):
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
    def __init__(self):
        self.twitter_get_user_timeline = TwitterGetUserTimelineModule()
        self.req = self.twitter_get_user_timeline.twitter.get(self.twitter_get_user_timeline.url, \
                                                              params = self.twitter_get_user_timeline.params)

    def producer_run(self):
        """
        Running Producer
        """
        self.twitter_get_user_timeline.twitter_method(self.req)
        global twiteet_queue
        global check_queue
        while True:
            if twiteet_queue not in check_queue.queue:
                try:
                    twiteet_queue.put(self.twitter_get_user_timeline.twitter_txt_dict)
                    check_queue.put(self.twitter_get_user_timeline.twitter_txt_dict)
                except twiteet_queue.Full:
                    print("Queue Full")
                    pass
                else:
                    log_text = "Produced "
                    print(log_text)
                    time.sleep(random.uniform(5, 8))

    def consumer_run(self):
        """
        Running Consumer
        """
        global twiteet_queue
        while True:
            try:
                twitter_txt_dict = twiteet_queue.get()
            except twiteet_queue.Empty:
                print("Queue Empty")
                pass
            else:
                log_text = "Consume "
                print(log_text)
                for k,v in twitter_txt_dict.items():
                    params = {"screen_name": k, "exclude_replies": False, "count": 10000}
                    req = self.twitter_get_user_timeline.twitter.get(self.twitter_get_user_timeline.url, params = params)
                    self.twitter_get_user_timeline.twitter_method(req, dict_flag=False, dict_value=v)
                # SQLite
                self.twitter_get_user_timeline.conn.commit()
                self.twitter_get_user_timeline.conn.close()
                twiteet_queue.task_done()
                # Setting the wait time, I refered to the bellow link
                #  https://www.w3.org/Protocols/HTTP-NG/http-prob.html
                time.sleep(random.uniform(5, 8))