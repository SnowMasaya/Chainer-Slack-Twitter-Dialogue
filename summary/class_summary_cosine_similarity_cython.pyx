#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import numpy as np


class ClassSummaryCosineSimilarityCython():
    """Class Summary class.

    This class is the summary class

    """

    def __init__(self, class_average_vector={}):
        """
        Args:
            word_list(list): you set the word list.
            wiki_vector: you set the wiki vector dictionary
            class_vector: you set the word class dictionary
        """
        self.__class_average_vector = class_average_vector
        self.COSIN_SIMILARITY_LIMIT = 0.5

    def summary_class_use_cosine_similarity(self):
        for class_name, vector in self.__class_average_vector.items():
            for class_name_check, vector_check in self.__class_average_vector.items():
                cosine_similarity_value = self.__cosine_similarity(vector, vector_check)
                print(class_name)
                print(class_name_check)
                print(cosine_similarity_value)
                """
                if cosine_similarity_value > self.COSIN_SIMILARITY_LIMIT:
                    print(class_name)
                    print(class_name_check)
                """


    def __cosine_similarity(self, vevtor1, vector2):
        """
        calculate the cosine similarity
        """
        try:
            return sum([a*b for a, b in zip(vevtor1, vector2)])/(sum(map(lambda x: x*x, vevtor1))**0.5 * sum(map(lambda x: x*x, vector2))**0.5)
        except ZeroDivisionError:
            return 0

