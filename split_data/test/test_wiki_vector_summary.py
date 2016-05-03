#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from input_file import InputFile
from split_synonym_class import SplitSynonymClass
from wiki_vector_summary import WikiVectorSummary
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))


class Test_WikiVectorSummary(unittest.TestCase):
    """Test wiki Vector class.

    """
    def setUp(self):
        """
        setting initial paramater
        Args:
            data: test file name
            split_module: setting the split_module instance
        """
        wiki_vector_file_name = APP_ROOT + '/../../Data/jawiki_vector/jawiki_vector.txt'
        self.word_net_file_name = APP_ROOT + '/../../Data/wnjpn-all.tab'
        self.input_module = InputFile(wiki_vector_file_name)

    def test_summary_class(self):
        """
        test make summary dict
        """
        self.input_module.input_fast_large_file()
        wiki_vector = self.input_module.get_vector()
        self.input_module = InputFile(self.word_net_file_name)
        self.input_module.input_special_format_file("\t")
        test_data = self.input_module.get_file_data()
        self.split_synonym_class = SplitSynonymClass(test_data)
        self.split_synonym_class.make_dict()
        # test all dict
        all_dict = self.split_synonym_class.get_all_dict()
        # test split dict
        split_dict = self.split_synonym_class.get_split_dict()
        self.wiki_vector_summary = WikiVectorSummary(all_dict, split_dict, wiki_vector)
        self.wiki_vector_summary.get_similler_word()
        split_dict = self.wiki_vector_summary.get_split_dict()
        for k, v in split_dict.items():
            fo = open(APP_ROOT + "/../../Data/test/" + k + ".txt", 'w')
            sys.stdout = fo
            print(v)
            fo.close()
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
