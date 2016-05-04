#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyximport
pyximport.install()
from class_summary_cython import ClassSummaryCython
from class_summary_cosine_similarity_cython import ClassSummaryCosineSimilarityCython
from split_data.input_file_cython import InputFileCython
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))
import re


class Test_ClassSummary(unittest.TestCase):
    """Test Class Summary class.

    """
    def setUp(self):
        """
        setting initial paramater
        Args:
            data: test file name
            split_module: setting the split_module instance
        """
        wiki_vector_file_name = APP_ROOT + '/../../Data/jawiki_vector/jawiki_vector.txt'
        self.input_module = InputFileCython(wiki_vector_file_name)

    def test_summary_class(self):
        """
        test make summary dict
        """
        self.input_module.input_fast_large_file()
        wiki_vector = self.input_module.get_vector()
        wn_summary_list = APP_ROOT + '/../../Data/wn_summary_list.txt'
        self.input_module = InputFileCython(wn_summary_list)
        self.input_module.input_special_format_file()
        file_list = self.input_module.get_file_data()
        count = 0
        class_word_vector = {}
        class_average_vector = {}
        for file in file_list:
            self.input_module = InputFileCython(APP_ROOT + "/../../Data/wn_summary/" + file.strip())
            self.input_module.input_special_format_file()
            if count == 0:
                class_summary = ClassSummaryCython(file.strip(), self.input_module.get_file_data(), wiki_vector)
            else:
                class_summary = ClassSummaryCython(file.strip(), self.input_module.get_file_data(), wiki_vector, class_word_vector, class_average_vector)
            class_word_vector, class_average_vector = class_summary.summary_class()
            fo = open(APP_ROOT + "/../../Data/test/" + file.strip() + "_vector.txt", 'w')
            sys.stdout = fo
            print(class_average_vector[file.strip()])
            fo.close()
            sys.stdout = sys.__stdout__
        class_summary_cosine_similarity_cython = ClassSummaryCosineSimilarityCython(class_average_vector)
        class_summary_cosine_similarity_cython.summary_class_use_cosine_similarity()


if __name__ == '__main__':
    unittest.main()
