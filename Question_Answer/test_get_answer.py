#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from os import path
APP_ROOT = path.dirname( path.abspath( __file__ ) )
from get_answer import GetAnswer


class Test_GetAnswer(unittest.TestCase):
    """regist the data into the elastic Search"""

    def setUp(self):
        # setting elastic search
        self.elastic_search = GetAnswer()

    def test_search(self):
        self.elastic_search.search_data("日総工産")
        test_json_data = {'abstract': '日総工産株式会社（にっそうこうさん）は、日本の企業。1971年2月3日創業、製造業分野における請負・派遣会社大手。', 'url': 'https://ja.wikipedia.org/wiki/%E6%97%A5%E7%B7%8F%E5%B7%A5%E7%94%A3', 'title': '日総工産'}
        self.assertEqual(test_json_data, self.elastic_search.search_result[0])


if __name__ == '__main__':
    unittest.main()