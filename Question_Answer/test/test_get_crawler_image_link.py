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
from get_crawler_image_link import GetCrawlerImageLink


class Test_GetCrawlerImageLink(unittest.TestCase):
    """
    Check contents similarity
    """

    def setUp(self):
        self.wiki_pedia_image_link = WikiPediaImageLink()
        self.get_crawler_image_link = GetCrawlerImageLink()

    def test_get_like_search(self):
        test_word = "Zundert"
        answer_list = [
            'https://upload.wikimedia.org/wikipedia/commons/b/b5/Zundert-City_Hall.JPG',
        ]
        self.wiki_pedia_image_link.search_like(test_word)
        self.get_crawler_image_link.crawler(self.wiki_pedia_image_link.image_data_list[0])
        self.assertListEqual(self.get_crawler_image_link.image_link_list, answer_list)


if __name__ == '__main__':
    unittest.main()