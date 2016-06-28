#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from split_data.input_file import InputFile
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))


class ClassSummary():
    """Class Summary class.

    This class is the summary class

    """

    def __init__(self, file_name, wiki_vector, input_path, output_path=""):
        """
        Args:
            word_list(list): you set the word list.
            wiki_vector: you set the wiki vector dictionary
            class_vector: you set the word class dictionary
        """
        self.__file_name = file_name
        self.input_path = input_path
        self.output_path = output_path
        self.output_flag = False
        if output_path != "":
            self.output_flag = True
        self.extension = "_vector.txt"
        self.input_module = InputFile(APP_ROOT + input_path + file_name)
        if file_name != "":
            self.input_module.input_special_format_file()
        self.__word_list = self.input_module.get_file_data()
        self.__wiki_vector = wiki_vector
        self.__class_word_vector = {}
        self.__word_vector = {}
        self.__average_vector = {}

    def summary_class(self):
        for word in self.__word_list:
            word = re.sub("\]|\[|\'|\s", "", word.strip())
            self.__add_wiki_vector(word.split(","))

    def summary_vector(self):
        self.__add_wiki_vector(self.__word_list)

    def summary_vector_word_list(self, word_list):
        self.__add_wiki_vector(word_list)

    def __add_wiki_vector(self, word_list):
        for word in word_list:
            if word in self.__wiki_vector:
                if word not in self.__word_vector:
                    self.__word_vector.update({word: self.__wiki_vector[word]})
        self.__calculate_average_vector()

    def __calculate_average_vector(self):
        average_list = []
        for word, vector in self.__word_vector.items():
            average_list.append(vector)
        average_vector = np.array(average_list)
        if average_vector != []:
            with open(APP_ROOT + self.output_path + self.__file_name.strip() + self.extension, 'w', encoding='utf-8') as fo:
                 self.__average_vector = np.mean(average_vector, axis=0).tolist()
                 if self.output_flag:
                     fo.write(str(self.__average_vector))
                     fo.write("\n")

    def get_average_vector(self):
        return self.__average_vector

