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
        config_file = "enviroment.yml"

        with open(config_file, encoding="utf-8") as cf:
            e = yaml.load(cf)
            twitter = Twitter(e["twitter"]["mecab"])

        self.tagger = MeCab.Tagger("-Owakati -d %s" % twitter.mecab)
        conn = sqlite3.connect('./twitter_data.db')
        self.cur = conn.cursor()
        self.class_word_vector = class_word_vector
        self.class_word_dict = self.__make_class_word_dict()

    def __make_class_word_dict(self):
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
        for file in file_list:
            os.remove("./data/" + file)
        for source_txt, replay_txt in self.cur.fetchall():
            class_name = self.__judge_class(source_txt, replay_txt)
            print(class_name)
            print(source_txt)
            print(replay_txt)
            source_file = open("./data/" + class_name + '_source_twitter_data.txt', 'a')
            replay_file = open("./data/" + class_name + '_replay_twitter_data.txt', 'a')
            replay_file.write(self.tagger.parse(source_txt).replace("\n", "") + '\n')
            source_file.write(self.tagger.parse(replay_txt).replace('\n', '') + '\n')
            source_file.close()
            replay_file.close()

    def __judge_class(self, source_txt, replay_txt):
        """
        Judge word class
        :param source_txt: twitter source text
        :param replay_txt: twitter replay text
        :return: most match class
        """
        class_match_rate = {}
        source_wakati_text = self.__mecab_method(source_txt.strip())
        replay_wakati_text = self.__mecab_method(replay_txt.strip())
        total_text = []
        total_text.extend(source_wakati_text)
        total_text.extend(replay_wakati_text)
        for class_name in self.class_word_vector.keys():
            word_match_count = self.__match_word_count(total_text, class_name)
            if class_name not in class_match_rate:
                class_match_rate.update({class_name: 1.0 * word_match_count / len(self.class_word_dict[class_name])})
        if max(class_match_rate.values()) == 0.0:
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
