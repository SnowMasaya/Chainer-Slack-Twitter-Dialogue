#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from os import path
APP_ROOT = path.dirname( path.abspath( __file__ ) )
import xml.etree.ElementTree
import json
import codecs


class WikiPediaXmlToJson():
    """
    Wikipedia xml data extract data and convert to the json format
    Data:
       https://dumps.wikimedia.org/jawiki/20160901/jawiki-20160901-abstract.xml
    """

    def __init__(self, wikipedia_abstract_xml):
        """
        Setting initial data
        """
        self.wikipedia_abstract_xml = wikipedia_abstract_xml
        self.wikipedia_abstract_json = wikipedia_abstract_xml.replace(".xml", "0.json")
        self.json_data = {}
        self.index_json = {}
        self.json_data_array = []
        self.extract_feed = "feed"
        self.extract_dict_array = ["title", "abstract", "url"]

    def input(self):
        """
        Get the data by xml format
        """
        self.xml_data = xml.etree.ElementTree.parse(self.wikipedia_abstract_xml).getroot()
        self.__extract_contents()

    def __extract_contents(self):
        """
        Get the contents below for regist the elasticsearch
        title
        abstract
        url
        :return:
        """
        index_count = 0
        file_index_count = 1
        if os.path.isfile(self.wikipedia_abstract_json):
            os.remove(self.wikipedia_abstract_json)
        for doc in self.xml_data:
            for extract_data in doc:
                if extract_data.tag in self.extract_dict_array:
                    # replace method for title extract
                    if extract_data.text is not None:
                        self.index_json.update({ "index" : { "_index" : "wikipedia", "_type" : "contents", "_id" : str(index_count) } })
                        self.json_data.update({extract_data.tag: extract_data.text.replace("Wikipedia: ", "")})
                    else:
                        self.index_json.update({ "index" : { "_index" : "wikipedia", "_type" : "contents", "_id" : str(index_count)  } })
                        self.json_data.update({extract_data.tag: extract_data.text})
            self.__output_json()
            self.json_data = {}
            index_count = index_count + 1
            """
            We have to reduce doc size for bulk insert (10k)
            Reference
               https://github.com/elastic/elasticsearch/issues/11899
            """
            if index_count % 10000 == 0:
                before_file_index_count = file_index_count - 1
                self.wikipedia_abstract_json =self.wikipedia_abstract_json.replace(str(before_file_index_count) + ".json", str(file_index_count) + ".json")
                print(self.wikipedia_abstract_json)
                file_index_count = file_index_count + 1

    def __output_json(self):
        """
        Make contents json
        :param json_out_put:
        :param data:
        :return:
        """
        with codecs.open(self.wikipedia_abstract_json, 'a', 'utf-8') as fo:
            fo.write(json.dumps(self.index_json, ensure_ascii=False))
            fo.write("\n")
            fo.write(json.dumps(self.json_data, ensure_ascii=False))
            fo.write("\n")