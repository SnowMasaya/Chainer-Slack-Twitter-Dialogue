#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from multi_thread_producer_consumer_twitter import ProducerConsumerThreadTwitter
from os import path
import threading
import argparse
APP_ROOT = path.dirname(path.abspath( __file__ ))

"""
This script for parallel command multi thread program
"""


if __name__ == '__main__':
    """


    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--consumer_size', '-c', default=30,
                        help='set consumer size')
    args = parser.parse_args()
    producerConsumerThreadTwitter = ProducerConsumerThreadTwitter()
    multi_thread_producer_twitter_instance = threading.Thread(target=producerConsumerThreadTwitter.producer_run)
    multi_thread_producer_twitter_instance.start()
    consumer_name = "producer"
    for index in range(int(args.consumer_size)):
        multi_thread_consumer_twitter_instance = threading.Thread(target=producerConsumerThreadTwitter.consumer_run, \
                                                                  name=consumer_name + str(index))
        multi_thread_consumer_twitter_instance.start()

