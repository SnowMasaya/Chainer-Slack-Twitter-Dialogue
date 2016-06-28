#!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3
from __future__ import division

import sqlite3
import MeCab
import yaml
from collections import namedtuple
import operator
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyximport
pyximport.install()
from split_data.input_file_cython import InputFileCython
from summary.class_summary import ClassSummary
from summary.class_summary_cosine_similarity import ClassCosineSimilarity
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))


class SqliteTwitterSummary(object):
    """
    Twitter Save to the SQLite
    """
    def __init__(self, class_word_vector):
        """
        Initial Setting
        Get the mecab dict by the yaml
        """
        Twitter = namedtuple("Twitter", ["mecab"])
        config_file = "enviroment_twitter.yml"

        with open(config_file, encoding="utf-8") as cf:
            e = yaml.load(cf)
            twitter = Twitter(e["twitter"]["mecab"])

        self.tagger = MeCab.Tagger("-Owakati -d %s" % twitter.mecab)
        conn = sqlite3.connect('./twitter_data.db')
        self.cur = conn.cursor()
        self.class_word_vector = class_word_vector
        self.class_average_vector = {}
        self.class_word_dict = self.make_class_word_dict()
        self.__initial_setting_vector()

    def __initial_setting_vector(self):
        # Wiki vector dict
        wiki_vector_file_name = APP_ROOT + '/../Data/jawiki_vector/jawiki_vector_delete_first.txt'
        self.input_module = InputFileCython(wiki_vector_file_name)
        self.input_module.input_fast_large_file()
        self.wiki_vector = self.input_module.get_vector()
        # Make average vector dict
        wiki_average_vector_file_name_list = APP_ROOT + '/../Data/wn_summary_multi_vector_list.txt'
        self.input_module = InputFileCython(wiki_average_vector_file_name_list)
        self.input_module.input_special_format_file()
        summary_vector_file_list = self.input_module.get_file_data()
        for file in summary_vector_file_list:
            read_file = APP_ROOT + "/../Data/wn_summary_multi_vector/" + file
            self.input_module = InputFileCython(read_file)
            self.input_module.input_file_str_list()
            summary_vector_file_list = self.input_module.get_file_data()
            class_name = file.replace("_summary.txt_vector.txt", "")
            if class_name not in self.class_average_vector:
                self.class_average_vector.update({class_name: summary_vector_file_list})
        self.class_summary = ClassSummary("", self.wiki_vector, "")
        self.cosine_similarity = ClassCosineSimilarity("", "")

    def make_class_word_dict(self):
        """
        make remake the data format
        """
        word_class_dict = {}
        for class_name, word_list in self.class_word_vector.items():
            word_dict = {}
            for word in word_list:
                if word not in word_dict:
                    word_dict.update({word: 1})
            if class_name not in word_class_dict:
                word_class_dict.update({class_name: word_dict})
        return word_class_dict

    def call_sql(self):
        """
        call SQlite and save the twitter in the SQLite
        """
        self.cur.execute("""SELECT source_txt, replay_txt FROM ms_rinna;""")
        file_list = os.listdir("./data/")
        #for file in file_list:
        #    os.remove("./data/" + file)
        for source_txt, replay_txt in self.cur.fetchall():
            # class_name = self.judge_class(source_txt, replay_txt)
            class_name = self.judge_class_wiki_vector(source_txt, replay_txt)
            print(class_name)
            print(source_txt)
            print(replay_txt)
            source_file = open("./data/" + class_name + '_source_twitter_data.txt', 'a')
            replay_file = open("./data/" + class_name + '_replay_twitter_data.txt', 'a')
            replay_file.write(self.tagger.parse(source_txt).replace("\n", "") + '\n')
            source_file.write(self.tagger.parse(replay_txt).replace('\n', '') + '\n')
            source_file.close()
            replay_file.close()

    def judge_class(self, source_txt, replay_txt=""):
        """
        Judge word class
        :param source_txt: twitter source text
        :param replay_txt: twitter replay text
        :return: most match class
        """
        class_match_rate = {}
        total_text = []
        source_wakati_text = self.__mecab_method(source_txt.strip())
        total_text.extend(source_wakati_text)
        if replay_txt != "":
            replay_wakati_text = self.__mecab_method(replay_txt.strip())
            total_text.extend(replay_wakati_text)
        for class_name in self.class_word_vector.keys():
            word_match_count = self.__match_word_count(total_text, class_name)
            if class_name not in class_match_rate:
                class_match_rate.update({class_name: 1.0 * word_match_count / len(self.class_word_dict[class_name])})
        if max(class_match_rate.values()) == 0.0:
            return "other"
        else:
            return max(class_match_rate.items(), key=operator.itemgetter(1))[0]

    def judge_class_wiki_vector(self, source_txt, replay_txt=""):
        """
        Judge word class by wiki vector
        :param source_txt: twitter source text
        :param replay_txt: twitter replay text
        :return: most match class
        """
        class_match_rate = {}
        total_text = []
        source_wakati_text = self.__mecab_method(source_txt.strip())
        total_text.extend(source_wakati_text)
        if replay_txt != "":
            replay_wakati_text = self.__mecab_method(replay_txt.strip())
            total_text.extend(replay_wakati_text)
        self.class_summary.summary_vector_word_list(total_text)
        summary_vector = self.class_summary.get_average_vector()
        for class_name, average_vector in self.class_average_vector.items():
            class_match_rate.update({class_name: self.cosine_similarity.cosine_similarity(summary_vector, average_vector)})
        print(class_match_rate)
        if max(class_match_rate.values()) <= 0.1:
            return "other"
        else:
            return max(class_match_rate.items(), key=operator.itemgetter(1))[0]

    def __mecab_method(self, text):
        """
        Call Mecab method split process and choose noum
        :param text:
        :return: only noum
        """
        res = self.tagger.parseToNode("".join(text))
        split_nonum = []
        while res:
            feature = res.feature.split(",")
            if feature[0] == u"名詞":
                split_nonum.append(feature[6])
            res = res.next
        return split_nonum

    def __match_word_count(self, total_text, class_name):
        """
        count matthing word word class
        :param total_text: source text and reply text
        :param class_name: choose class name
        :return: matthing count
        """
        word_match_count = 0
        for word in total_text:
            if word in self.class_word_dict[class_name]:
                word_match_count = word_match_count + 1
        return word_match_count
