#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from input_file import InputFile
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))


class Test_InputFile(unittest.TestCase):
    """Test Input file class.

    """
    def setUp(self):
        """
        setting initial paramater
        Args:
            file name: test file name
            input_module: setting the input_module instance
        """
        file_name = APP_ROOT + '/../../Data/wnjpn-all.tab'
        self.input_module = InputFile(file_name)

    def test_input_special_format_file(self):
        """
        test input tsv file
        """
        self.input_module.input_special_format_file("\t")
        test_data = self.input_module.get_file_data()
        self.assertEqual(test_data[1], ['00001740-a', '優秀', 'XXXX'])

if __name__ == '__main__':
    unittest.main()