#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyximport
pyximport.install()
from split_data.input_file_cython import InputFileCython
from class_summary_exclude_cython import ClassSummaryExcludeCython
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))
import re


class Test_ClassSummaryExclude(unittest.TestCase):
    """Test Class Summary class.

    """
    def setUp(self):
        """
        setting initial paramater
        Args:
            data: test file name
            split_module: setting the split_module instance
        """
        wn_summary_list = APP_ROOT + '/../../Data/wn_total_summary_list.txt'
        self.input_module = InputFileCython(wn_summary_list)
        self.input_module.input_special_format_file()
        self.class_summary_exclude = ClassSummaryExcludeCython()

    def test_summary_class(self):
        """
        test make summary dict
        """
        file_list = self.input_module.get_file_data()
        OUT_PUT_PATH = APP_ROOT + "/../../Data/wn_total_summary_51519_limit05_out_put/"
        for file in file_list:
            self.input_module = InputFileCython(APP_ROOT + "/../../Data/wn_total_summary_51519_limit05/" + file.strip())
            self.input_module.input_special_format_file()
            self.class_summary_exclude.exclude_data(OUT_PUT_PATH, file.strip(), self.input_module.get_file_data())


if __name__ == '__main__':
    unittest.main()
