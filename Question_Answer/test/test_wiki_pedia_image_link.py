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
from wiki_pedia_image_link import WikiPediaImageLink


class Test_WikiPediaImageLink(unittest.TestCase):
    """
    Check contents similarity
    """

    def setUp(self):
        self.wiki_pedia_image_link = WikiPediaImageLink()

    def test_get_like_search(self):
        test_word = "Zundert"
        answer_list = [
            'https://en.wikipedia.org/wiki/File:Zundert-City_Hall.JPG',
            'https://en.wikipedia.org/wiki/File:Zundert_church.JPG',
            'https://en.wikipedia.org/wiki/File:Zundert_gravestone_van_Gogh.JPG'
        ]
        self.wiki_pedia_image_link.search_like(test_word)
        self.assertListEqual(self.wiki_pedia_image_link.image_data_list, answer_list)

if __name__ == '__main__':
    unittest.main()