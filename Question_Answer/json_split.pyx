#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname("__file__"), "."))
from os import path
APP_ROOT = path.dirname(path.abspath("__file__"))
import pyximport
pyximport.install()


class JsonSplit():
    """
    Json Split Script for Elasticsearch
    """

    def __init__(self, file_name):
        """
        Setting initial paramater
        :param file_name(string): file name
        """
        self.file_name = file_name
        self.data = []
        self.index_check = "{\"index"
        self.abstract_check = "{\"abstract"
        self.index_count = 0
        self.limit_out_put = 10000
        self.file_output_counter = 0
        self.out_put_file_name = APP_ROOT + "/../Data/wiki_image/enwiki-20080103-abstract"
        if os.path.isfile(self.out_put_file_name + "[1-9]" + ".json"):
            os.remove(self.out_put_file_name + "[1-9]" + ".json")

    def input(self):
        """
        input file data
        """
        with open(self.file_name) as f:
            self.data = list(map(lambda s: s.strip(), f.readlines()))
        f.close()
        self.__split()

    def __split(self):
        """
        split json data
        :return:
        """
        for data in self.data:
            if self.index_check in data:
                if (self.index_count % 10000) == 0:
                    self.file_output_counter = self.file_output_counter + 1
                replace_index = "\"_index\": \"wikipedia_image\""
                replace_count = "{\"_id\": \"" + str(self.index_count) + "\""
                replace_data = data.replace("{\"_id\": \"0\"", replace_count)
                replace_data = replace_data.replace("\"_index\": \"wikipedia\"", replace_index)
                self.__output(replace_data)
                self.index_count = self.index_count + 1
            elif self.abstract_check in data:
                self.__output(data)

    def __output(self, data):
        """
        Output json data
        :param data(string): replace index number data
        """
        out_put_file_name = self.out_put_file_name + str(self.file_output_counter) + ".json"
        with open(out_put_file_name, "a") as fw:
            fw.write(data)
            fw.write("\n")
        fw.close()

