#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SplitSynonymClass():
    """Split Synonym class.

    This class is split synonym
    """

    def __init__(self, data):
        """
        Args:
            data (list): input the word net data.
        """
        self.__data = data
        self.__all_dict = {}
        self.__split_dict = {}

    def make_dict(self):
        """
        split class
        """
        data_class = ""
        for each_data in self.__data:
            data_class = each_data[0]
            word = each_data[1]
            self.__make_all_split_dict(data_class, word)

    def __make_all_split_dict(self, data_class, word):
        """
        split class
        Args:
            word(str): word net word()
            data_class(str): word net class
        """
        word_list = []
        # regist all dict
        if word not in self.__all_dict:
            self.__all_dict.update({word: data_class})
        if data_class not in self.__split_dict:
            word_list.append(word)
            self.__split_dict.update({data_class: word_list})
        else:
            word_list = self.__split_dict[data_class]
            word_list.append(word)
            self.__split_dict.update({data_class: word_list})

    def get_all_dict(self):
        """get the all dict"""
        return self.__all_dict

    def get_split_dict(self):
        """get the split dict"""
        return self.__split_dict
