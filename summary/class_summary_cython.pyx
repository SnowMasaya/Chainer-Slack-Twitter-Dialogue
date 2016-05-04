#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import numpy as np


class ClassSummaryCython():
    """Class Summary class.

    This class is the summary class

    """

    def __init__(self, file_name, word_list, wiki_vector, class_word_vector={},class_average_vector={}):
        """
        Args:
            word_list(list): you set the word list.
            wiki_vector: you set the wiki vector dictionary
            class_vector: you set the word class dictionary
        """
        self.__file_name = file_name
        self.__word_list = word_list
        self.__wiki_vector = wiki_vector
        self.__class_word_vector = class_word_vector
        self.__word_vector = {}
        self.__class_average_vector = class_average_vector

    def summary_class(self):
        for word in self.__word_list:
            word = re.sub("\]|\[|\'|\s", "", word.strip())
            self.__add_wiki_vector(word.split(","))
        return self.__class_word_vector, self.__class_average_vector

    def __add_wiki_vector(self, word_list):
        for word in word_list:
            if word in self.__wiki_vector:
                if word not in self.__word_vector:
                    self.__word_vector.update({word: self.__wiki_vector[word]})
        if self.__file_name not in self.__class_word_vector:
            self.__class_word_vector.update({self.__file_name: self.__word_vector})
        self.__calculate_average_vector()

    def __calculate_average_vector(self):
        for class_name, word_vector in self.__class_word_vector.items():
            self.__calculate_average_vector_numpy(word_vector)

    def __calculate_average_vector_numpy(self, word_vector):
        average_list = []
        for word, vector in word_vector.items():
            average_list.append(vector)
        average_vector = np.array(average_list)
        if self.__file_name not in self.__class_average_vector and average_vector != []:
            self.__class_average_vector.update({self.__file_name: np.mean(average_vector, axis=0)})
            print(len(self.__class_average_vector))

