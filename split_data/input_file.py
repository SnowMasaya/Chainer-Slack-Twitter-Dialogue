#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import csv
csv.field_size_limit(1760000000)


class InputFile():
    """Input file class.

    This class read the a varity of file such as the csv, txt, tsv
    If you input the file, you only use the this class
    """

    def __init__(self, file_name):
        """
        Args:
            file_name (str): you set the file name.
        """
        self.__file_name = file_name
        self.__data = []
        self.__word_vector = {}

    def input_special_format_file(self, input_delimiter=""):
        """
        Examples:
            csv file
                input_special_format_file(",")
            tsv file
                input_special_format_file("\t")
        Args:
            input_delimiter: you set the delimiter.
        """
        f = codecs.open(self.__file_name, 'r', 'utf-8')
        file = csv.reader(f, delimiter = input_delimiter)
        for line in file:
            self.__data.append(line)
        f.close()

    def input_fast_large_file(self):
        with open(self.__file_name, encoding='utf-8', errors='ignore') as FileObj:
            for lines in FileObj:
                word_vector = lines.strip().split(" ")
                word = word_vector.pop(0)
                word_vector = list(map(float, word_vector))
                if word not in self.__word_vector:
                   self.__word_vector.update({word: word_vector})

    def get_file_data(self):
        """If you get the file data you call this function."""
        return self.__data

    def get_vector(self):
        """If you get the vector file data you call this function."""
        return self.__word_vector
