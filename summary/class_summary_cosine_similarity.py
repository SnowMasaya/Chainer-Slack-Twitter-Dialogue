#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import sys


class ClassCosineSimilarity():
    """Class Summary class.

    This class is the summary class because a lot word class(71920 class)

    """

    def __init__(self, class_word, class_average_vector):
        """
        Args:
            class_word(dict): you set the class word dict
            class_average_vector(dict): you set the class average vector
        """
        self.__class_word = class_word
        self.__class_average_vector = class_average_vector
        self.COSIN_SIMILARITY_LIMIT = 0.6
        self.output_path = "/Users/masayaogushi/PycharmProjects/Study/Chainer-Slack-Twitter-Dialogue/Data/wn_total_summary/"
        self.extension = "_summary.txt"

    def summary_class_use_cosine_similarity(self):
        """
        summary method
        """
        # deep copy used reason why dict size change
        class_average_vector = copy.deepcopy(self.__class_average_vector)
        check_class_average_vector = copy.deepcopy(self.__class_average_vector)
        print(len(self.__class_word))
        count = 0
        for class_name, vector in class_average_vector.items():
            for class_name_check, vector_check in check_class_average_vector.items():
                if class_name != class_name_check and class_name in self.__class_word:
                    cosine_similarity_value = self.cosine_similarity(vector, vector_check)
                    if cosine_similarity_value > self.COSIN_SIMILARITY_LIMIT:
                        self.__summary_class(class_name, class_name_check)
                        self.__delete_class(class_name_check)
                count = count + 1

        print(len(self.__class_word))
        self.__out_put_file()

    def __out_put_file(self):
        """
        Make output file
        """
        for class_name, word in self.__class_word.items():
            fo = open(self.output_path + class_name.strip() + self.extension, 'w')
            sys.stdout = fo
            print(word)
            fo.close()
            sys.stdout = sys.__stdout__

    def cosine_similarity(self, vevtor1, vector2):
        """
        calculate the cosine similarity
        Args:
            vector1(list): you set the word class average vector
            vector2(list): you set the word class average vector for compare
        """
        try:
            return sum([a*b for a, b in zip(vevtor1, vector2)])/(sum(map(lambda x: x*x, vevtor1))**0.5 * sum(map(lambda x: x*x, vector2))**0.5)
        except ZeroDivisionError:
            return 0

    def __summary_class(self, class_name, class_name_check):
        """
        summary word class and append word list
        Args:
            class_name(str): you set the word class name
            class_name_check(str): you set the word class name for summary
        """
        word_list = []
        if class_name in self.__class_word:
            [word_list.append(word.replace(" ", "")) for word in self.__class_word[class_name]]
        if class_name_check in self.__class_word:
            [word_list.append(word.replace(" ", "")) for word in self.__class_word[class_name_check]]
        self.__class_word.update({class_name: word_list})

    def __delete_class(self, class_name_check):
        """
        delete the similiarty word class
        Args:
            class_name_check(str): you set the delete word class
        """
        if class_name_check in self.__class_average_vector:
            del self.__class_average_vector[class_name_check]
        if class_name_check in self.__class_word:
            del self.__class_word[class_name_check]


