#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from multi_thread_producer_consumer_twitter_async import ProducerConsumerThreadTwitterAsync
from os import path
import argparse
import asyncio
APP_ROOT = path.dirname(path.abspath( __file__ ))

"""
This script for parallel command multi thread program
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    producerConsumerThreadTwitterAsync = ProducerConsumerThreadTwitterAsync()
    loop = asyncio.get_event_loop()

    #Producer
    loop.create_task(producerConsumerThreadTwitterAsync.producer_run())

    #Consumer
    loop.create_task(producerConsumerThreadTwitterAsync.consumer_run())
    loop.run_forever()
    loop.close()


