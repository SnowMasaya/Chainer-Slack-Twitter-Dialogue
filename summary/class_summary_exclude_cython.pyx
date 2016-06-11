#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class ClassSummaryExcludeCython():
    """Class Summary Exclude class.

    This class is Choosing the class data

    """

    def __init__(self):
        """
        Initial setting
        parama: limit
        """
        self.limit = 1000

    def exclude_data(self, OUT_PUT_PATH, file_name, word_list):
        """
        Exclude metho
        :param word_list(str) : you setting the word str
        Example
            ["['ぽんと', ' むざと', ' 惜しげもなく', ' 惜し気もなく', ' 惜し気も無く', ' 惜気もなく']\n"]
        """

        word_list = self.__remake_list(word_list)
        if len(word_list) > 1000:
            with open(OUT_PUT_PATH + file_name, "w") as file:
                for word in word_list:
                    file.write(word.replace(" ", "") + "\n")

    def __remake_list(self, word_list):
        return list(set(re.sub("\]|\[|\'", "", word_list[0].strip()).split(",")))

