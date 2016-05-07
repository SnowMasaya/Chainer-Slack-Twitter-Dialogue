#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import linalg, mat, dot
import numpy
import sys


class WikiVectorSummaryCython():
    """Wiki Vector Summary class.

    This class is the summary word class

    """

    def __init__(self, all_dict, split_dict, wiki_vector):
        """
        Args:
            file_name (str): you set the wiki vector file name.
        """
        self.__all_dict = all_dict
        self.__split_dict = split_dict
        self.__wiki_vector = wiki_vector
        self.__data = []
        self.data_class = ""
        self.wiki_word = ""
        self.missing_word = {}
        self.word_net_vector = {}
        self.class_average_vector = {}
        self.COSIN_SIMILARITY_LIMIT = 0.6
        self.delete_wiki_data = []
        self.average_list = []

    def get_similler_word(self):
        """
        Word Word Net Summary and Add wiki vector word for
        :return:
        """
        watch_count = 0
        for word, self.data_class in self.__all_dict.items():
            watch_count = watch_count + 1
            if watch_count % 100 == 0:
                print(watch_count)
                print(len(self.__all_dict))
            if word in self.__wiki_vector:
                self.__check_wiki_vector(word)
                print("--------------------------------------------------------------------")
                print(len(self.__split_dict))
        self.__make_average_dict()

    def __make_average_dict(self):
        for self.data_class, word_list in self.__split_dict.items():
            for word in word_list:
                if word in self.__wiki_vector:
                    self.word_net_vector.update({word: self.__wiki_vector[word]})
            self.__calculate_average_vector(self.data_class)
            self.word_net_vector = {}
        self.__add_wiki_word()

    def __check_wiki_vector(self, word):
        """
        Check wiki vector and word net word
        :param word:
        :return:
        """
        missing_word_list = []
        for self.wiki_word, vector in self.__wiki_vector.items():
            if self.wiki_word in self.__all_dict:
                cosine_similarity = self.__cosine_similarity(self.__wiki_vector[word], vector)
                self.__cosine_similarity_judge(cosine_similarity)
            else:
                missing_word_list.append(self.wiki_word)
        if self.data_class not in self.delete_wiki_data:
            self.missing_word.update({self.data_class: missing_word_list})
        else:
            for delete in self.delete_wiki_data:
                if delete in self.missing_word:
                    del self.missing_word[delete]

    def __cosine_similarity_judge(self, cosine_similarity):
        """
        The cosigne similarty word check
        :param cosine_similarity:
        :return:
        """
        if self.data_class in self.__split_dict:
            if cosine_similarity > self.COSIN_SIMILARITY_LIMIT and self.wiki_word not in self.__split_dict[self.data_class]:
                self.__sumary_dict()

    def __sumary_dict(self):
        """
        Summary Word Net Class for Make the topic dict
        :return:
        """
        wiki_data_class = self.__all_dict[self.wiki_word]
        # add word list wiki word class
        if wiki_data_class != self.data_class and wiki_data_class in self.__split_dict:
            [self.__split_dict[self.data_class].append(word) for word in self.__split_dict[wiki_data_class] if word not in self.__split_dict[self.data_class]]
            del self.__split_dict[wiki_data_class]
            self.delete_wiki_data.append(wiki_data_class)

    def __cosine_similarity(self, vector1, vector2):
        """
        calculate the cosine similarity
        """
        if len(vector1) != len(vector2):
            return 0
        cosine_vector1 = mat(vector1)
        cosine_vector2 = mat(vector2)
        try:
            return dot(cosine_vector1, cosine_vector2.T) / linalg.norm(cosine_vector1) / linalg.norm(cosine_vector2)
        except ZeroDivisionError:
            return 0

    def __calculate_average_vector(self, word_class):
        """
        Calculate the Average for each class Because calculate consine similarty for wiki word
        :param word_class:
        :return:
        """
        average_list = []
        for word, vector in self.word_net_vector.items():
            average_list.append(vector)
        if average_list != []:
            average_vector = numpy.mean(average_list, axis=0)
            self.class_average_vector.update({word_class: average_vector})

    def __add_wiki_word(self):
        """
        Add cosine similler word of wiki vector
        :return:
        """
        for word_class, word_list in self.missing_word.items():
            for word in word_list:
                self.__check_word_similitary(word_class, self.__wiki_vector[word], word)

    def __check_word_similitary(self, word_class, vector, word):
        """
        check word cosine similarty and make the split dict
        :param word_class:
        :param vector:
        :param word:
        """
        cosine_similarity = 0
        if word_class not in self.__split_dict:
            return
        if word not in self.__split_dict[word_class]:
            cosine_similarity = self.__cosine_similarity(self.class_average_vector[word_class], vector)
        if cosine_similarity > self.COSIN_SIMILARITY_LIMIT:
            self.__split_dict[word_class].append(word)

    def get_split_dict(self):
        """get the split dict"""
        return self.__split_dict

    def get_wiki_average_vector(self):
        """get the split dict"""
        return self.class_average_vector
