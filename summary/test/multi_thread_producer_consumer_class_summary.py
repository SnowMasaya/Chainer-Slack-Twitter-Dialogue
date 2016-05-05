#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from producer_consumer_class_summary import ProducerConsumerClassSummary
import pyximport
pyximport.install()
from split_data.input_file_cython import InputFileCython
from os import path
import threading
APP_ROOT = path.dirname(path.abspath( __file__ ))

"""
This script for parallel command multi thread program
"""


if __name__ == '__main__':
    """
    args
       -r: setting word net link list
           Example:
               '/../../Data/wn_summary_list.txt'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--read_word_net_list_file', '-r', default='',
                        help='set word net list file')
    args = parser.parse_args()
    #  Word Net File
    wn_summary_split_list = APP_ROOT + "/../../Data/" + args.read_word_net_list_file
    input_module = InputFileCython(wn_summary_split_list)
    input_module.input_special_format_file()
    file_list = input_module.get_file_data()
    # Wiki Vector
    wiki_vector_file_name = APP_ROOT + '/../../Data/jawiki_vector/jawiki_vector.txt'
    input_module = InputFileCython(wiki_vector_file_name)
    input_module.input_fast_large_file()
    wiki_vector = input_module.get_vector()

    producerConsumer = ProducerConsumerClassSummary()
    multi_thread_producer_crawl_instance = threading.Thread(target=producerConsumer.producer_run, args=([file_list]))
    multi_thread_consumer_crawl_instance = threading.Thread(target=producerConsumer.consumer_run, args=([wiki_vector]))
    multi_thread_producer_crawl_instance.start()
    multi_thread_consumer_crawl_instance.start()