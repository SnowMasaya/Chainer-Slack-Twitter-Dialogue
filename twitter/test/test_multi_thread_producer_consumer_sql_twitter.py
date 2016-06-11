#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from multi_thread_producer_consumer_sql_twitter import ProducerConsumerThreadSqlTwitter
from os import path
import threading
APP_ROOT = path.dirname(path.abspath( __file__ ))

"""
This script for parallel command multi thread program
"""


if __name__ == '__main__':
    """


    """
    producerConsumerThreadSqlTwitter = ProducerConsumerThreadSqlTwitter()
    multi_thread_producer_twitter_instance = threading.Thread(target=producerConsumerThreadSqlTwitter.producer_run)
    multi_thread_consumer_twitter_instance = threading.Thread(target=producerConsumerThreadSqlTwitter.consumer_run)
    multi_thread_producer_twitter_instance.start()
    multi_thread_consumer_twitter_instance.start()


