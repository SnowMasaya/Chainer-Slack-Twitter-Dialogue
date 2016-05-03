#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from input_file import InputFile
from split_synonym_class import SplitSynonymClass
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))


class Test_SplitSynonymClass(unittest.TestCase):
    """Test split file class.

    """
    def setUp(self):
        """
        setting initial paramater
        Args:
            data: test file name
            split_module: setting the split_module instance
        """
        file_name = APP_ROOT + '/../../Data/wnjpn-all.tab'
        self.input_module = InputFile(file_name)

    def test_make_dict(self):
        """
        test make split dict and all dict
        """
        self.input_module.input_special_format_file("\t")
        test_data = self.input_module.get_file_data()
        self.split_synonym_class = SplitSynonymClass(test_data)
        self.split_synonym_class.make_dict()
        # test all dict
        all_dict = self.split_synonym_class.get_all_dict()
        self.assertEqual(all_dict['木っ葉'], "00377169-n")
        self.assertEqual(len(self.split_synonym_class.get_all_dict()), 146517)
        # test split dict
        split_dict = self.split_synonym_class.get_split_dict()
        self.assertEqual(split_dict['02927303-a'], ['アメリカ大陸の', '北アメリカの', '南アメリカの', '南北アメリカ原産の'])
        self.assertEqual(len(self.split_synonym_class.get_split_dict()), 75771)
        print(split_dict["00377169-n"])



if __name__ == '__main__':
    unittest.main()