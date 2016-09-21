#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname("__file__"), "."))
from os import path
APP_ROOT = path.dirname(path.abspath("__file__"))
import urllib.request
from bs4 import BeautifulSoup


class GetCrawlerImageLink():
    """
    Wikipedia get the image link by the crawler
    """

    def __init__(self):
        self.html = ""
        self.https_domain = "https:"
        self.image_link_list = []

    def crawler(self, url):
        """
        Crawlering the link
        :param url(string): image link
        :return:
        """
        try:
            resource = urllib.request.urlopen(url)
            self.html = resource.read()
            self.__parse()
            resource.close
            return True
        except urllib.error.HTTPError as err:
            print("HTTPError: " + str(url) + str(err))
            return None
        except urllib.error.URLError as err:
            print("URLError: " + str(url) + str(err))
            return None

    def __parse(self):
        """
        Get the elements
        Reference
            https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        :return:
        """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        for link in self.soup.find_all('img'):
            try:
                image_link = link.get('srcset')
                self.__check_mage_link(image_link)
            except:
                print("Small Data and static icon and Not Get the Data")
                return None

    def __check_mage_link(self, image_link):
        """
        Check Small Data and static icon and Not Get the Data
        :param image_link:
        :return:
        """
        if image_link is not None and "thumb" not in image_link and "static" not in image_link:
            if self.https_domain not in image_link:
                self.image_link_list.append(self.https_domain + image_link.split(" ")[0])
            else:
                self.image_link_list.append(image_link.split(" ")[0])

