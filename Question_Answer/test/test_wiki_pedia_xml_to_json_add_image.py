#!/usr/bin/env python
#coding: utf8
import unittest
import sys
import os
from os import path
sys.path.append(os.path.join(os.path.dirname("__file__"), "./../"))
sys.path.append(os.path.join(os.path.dirname("__file__"), "."))
APP_ROOT = path.dirname(path.abspath(__file__))
from wiki_pedia_xml_to_json import WikiPediaXmlToJson
import filecmp


class Test_WikiPediaXmlToJson(unittest.TestCase):
    """
    Check contents similarity
    """

    def setUp(self):
        """
        :return:
        """
        self.wikipedia_abstract_xml = APP_ROOT + "/../../Data/wiki_image/enwiki-20080103-abstract_part.xml"
        self.wiki_pedia_xml_to_json = WikiPediaXmlToJson(self.wikipedia_abstract_xml)
        self.answer_data = APP_ROOT + "/../../Data/wiki_image/enwiki-20080103-abstract_part.json"
        self.correct_data = APP_ROOT + "/../../Data/wiki_image/answer_image.json"

    def test_extract_data(self):
        self.wiki_pedia_xml_to_json.input(image_Flag=True)

if __name__ == '__main__':
    unittest.main()