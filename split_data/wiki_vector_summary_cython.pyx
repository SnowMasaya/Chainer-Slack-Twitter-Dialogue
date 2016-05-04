#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct


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
        self.COSIN_SIMILARITY_LIMIT = 0.5

    def get_similler_word(self):
        watch_count = 0
        for word, self.data_class in self.__all_dict.items():
            watch_count = watch_count + 1
            print(watch_count)
            print(len(self.__all_dict))
            if word in self.__wiki_vector:
                self.__check_wiki_vector(word)
                print("--------------------------------------------------------------------")
                print(len(self.__split_dict))

    def __check_wiki_vector(self, word):
        for self.wiki_word, vector in self.__wiki_vector.items():
            cosine_similarity = self.__cosine_similarity(self.__wiki_vector[word], vector)
            self.__cosine_similarity_judge(cosine_similarity)

    def __cosine_similarity_judge(self, cosine_similarity):
        if self.data_class in self.__split_dict:
            if cosine_similarity > self.COSIN_SIMILARITY_LIMIT and self.wiki_word not in self.__split_dict[self.data_class]:
                self.__sumary_dict()

    def __sumary_dict(self):
        if self.wiki_word in self.__all_dict:
            wiki_data_class = self.__all_dict[self.wiki_word]
            # add word list wiki word class
            if wiki_data_class != self.data_class and wiki_data_class in self.__split_dict:
                [self.__split_dict[self.data_class].append(word) for word in self.__split_dict[wiki_data_class] if word not in self.__split_dict[self.data_class]]
                del self.__split_dict[wiki_data_class]
        else:
            self.__split_dict[self.data_class].append(self.wiki_word)

    def __cosine_similarity(self, vevtor1, vector2):
        """
        calculate the cosine similarity
        """
        try:
            return sum([a*b for a, b in zip(vevtor1, vector2)])/(sum(map(lambda x: x*x, vevtor1))**0.5 * sum(map(lambda x: x*x, vector2))**0.5)
        except ZeroDivisionError:
            return 0

    def get_split_dict(self):
        """get the split dict"""
        return self.__split_dict
