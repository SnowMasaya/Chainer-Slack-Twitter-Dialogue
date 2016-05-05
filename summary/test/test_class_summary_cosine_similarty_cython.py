#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyximport
pyximport.install()
from class_summary_cosine_similarity_cython import ClassSummaryCosineSimilarityCython
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
        wn_summary_list = APP_ROOT + '/../../Data/wn_summary_list.txt'
        self.input_module = InputFileCython(wn_summary_list)
        self.input_module.input_special_format_file()

    def test_summary_class(self):
        """
        test make summary dict
        """
        file_list = self.input_module.get_file_data()
        wn_average_vector_list = APP_ROOT + '/../../Data/wn_average_vector_list_part.txt'
        self.input_module = InputFileCython(wn_average_vector_list)
        self.input_module.input_special_format_file()
        vector_list = self.input_module.get_file_data()
        class_word_vector = {}
        class_average_vector = {}
        for file in file_list:
            self.input_module = InputFileCython(APP_ROOT + "/../../Data/wn_summary/" + file.strip())
            self.input_module.input_special_format_file()
            if file.strip() not in class_word_vector:
                word_list = re.sub("\]|\[|\'", "", self.input_module.get_file_data()[0].strip())
                class_word_vector.update({file.strip().replace(".txt", ""): word_list.split(",")})
        for vector in vector_list:
            #self.input_module = InputFileCython(APP_ROOT + "/../../Data/wn_summary_multi/" + vector.strip())
            self.input_module = InputFileCython(APP_ROOT + "/../../Data/test/" + vector.strip())
            self.input_module.input_special_format_file()
            vector_list = []
            if vector.strip() not in class_average_vector:
                for value in self.input_module.get_file_data():
                    value = re.sub("\]|\[|\'", "", value.strip())
                    [vector_list.append(each_value) for each_value in value.split(" ") if each_value != ""]
                    vector_list = list(map(float, vector_list))
                class_average_vector.update({vector.strip().replace(".txt_vector.txt", ""): vector_list})
        class_summary_cosine_similarity_cython = ClassSummaryCosineSimilarityCython(class_word_vector, class_average_vector)
        class_summary_cosine_similarity_cython.summary_class_use_cosine_similarity()


if __name__ == '__main__':
    unittest.main()
