#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from sqlite_twitter_summary import SqliteTwitterSummary
import pyximport
pyximport.install()
from split_data.input_file_cython import InputFileCython
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))
import re

class Test_ClassSummaryCosineSimilarty(unittest.TestCase):
    """Test Class Summary class.

    """
    def setUp(self):
        """
        setting initial paramater
        Args:
            data: test file name
            split_module: setting the split_module instance
        """
        wn_summary_list = APP_ROOT + '/../../Data/wn_total_summary_51519_limit05_out_put_list.txt'
        self.input_module = InputFileCython(wn_summary_list)
        self.input_module.input_special_format_file()

    def test_summary_class(self):
        """
        test make summary dict
        """
        file_list = self.input_module.get_file_data()
        class_word_vector = {}
        for file in file_list:
            self.input_module = InputFileCython(APP_ROOT + "/../../Data/wn_total_summary_51519_limit05_out_put/" + file.strip())
            self.input_module.input_special_format_file()
            if file.strip() not in class_word_vector:
                word_list = (list(map(lambda x:x.strip(), self.input_module.get_file_data())))
                class_word_vector.update({file.strip().replace("_summary.txt", ""): word_list})
        sqlite_twitter_cython = SqliteTwitterSummary(class_word_vector)
        sqlite_twitter_cython.call_sql()


if __name__ == '__main__':
    unittest.main()
