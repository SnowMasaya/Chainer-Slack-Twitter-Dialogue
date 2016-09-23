#!/usr/bin/env python
#coding: utf8
import unittest
import sys
import os
from os import path
sys.path.append(os.path.join(os.path.dirname("__file__"), "./../"))
sys.path.append(os.path.join(os.path.dirname("__file__"), "."))
APP_ROOT = path.dirname(path.abspath(__file__))
import pyximport
pyximport.install()
from json_split import JsonSplit
import filecmp


class Test_JsonSplit(unittest.TestCase):
    """
    Check json_split
    """

    def setUp(self):
        self.split_json_file = APP_ROOT + "/../../Data/wiki_image/enwiki-20080103-abstract0.json"
        self.answer_json = APP_ROOT + "/../../Data/wiki_image/answer_json_split1.json"
        self.out_json = APP_ROOT + "/../../Data/wiki_image/answer_json_split1.json"

    def test_split_data(self):
        self.json_split = JsonSplit(self.split_json_file)
        self.json_split.input()
        self.assertEqual(filecmp.cmp(self.answer_json, self.out_json), True)

if __name__ == '__main__':
    unittest.main()