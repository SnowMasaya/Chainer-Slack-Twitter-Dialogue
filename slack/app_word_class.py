import time
from slack_model import SlackModel
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from EncoderDecoderModelAttention import EncoderDecoderModelAttention
from Attention.attention_dialogue import AttentionDialogue
from chainer import serializers
from util.vocabulary import Vocabulary
import MeCab
from util.XP import XP
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import pyximport
pyximport.install()
from split_data.input_file_cython import InputFileCython
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))
import re
import operator


class SlackApp():
    """
    Slack Call app
    You preapre the chainer model, You execute the bellow command, you can play the dialogue app
    Example
        python app.py
    """

    def __init__(self, data_model):
        """
        Iniital Setting
        :param data_model: Setting Slack Model. Slack Model has the a lot of paramater
        """
        self.slack_channel = data_model.slack_channel
        self.data = ""
        self.parameter = data_model.parameter_dict
        self.model_name = "../model/ChainerDialogue"
        self.generation_limit = 200
        """
        We confirm channel number
        https://api.slack.com/methods/channels.list
        """
        self.chan = data_model.chan
        self.usr = data_model.user
        self.mecab_dict = data_model.mecab_dict
        self.Mecab = MeCab.Tagger("-Owakati -d %s" % self.mecab_dict)
        XP.set_library(False, 0)
        self.XP = XP
        wn_summary_list = APP_ROOT + '/../Data/wn_total_summary_list.txt'
        self.input_module = InputFileCython(wn_summary_list)
        self.input_module.input_special_format_file()
        file_list = self.input_module.get_file_data()
        self.class_word_vector = self.__make_class_word_vector(file_list)
        self.word_class_dict = self.__make_class_word_dict()
        self.word_class = ""

    def __make_class_word_vector(self, file_list):
        """
        Make class word vector dict
        :param file_list:
        :return:
        """
        class_word_vector = {}
        for file in file_list:
            self.input_module = InputFileCython(APP_ROOT + "/../Data/wn_summary/" + file.strip())
            self.input_module.input_special_format_file()
            if file.strip() not in class_word_vector:
                word_list = re.sub("\]|\[|\'", "", self.input_module.get_file_data()[0].strip())
                class_word_vector.update({file.strip().replace(".txt", ""): word_list.split(",")})
        return class_word_vector

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

    def call_method(self):
        """
        Slack api call
        1: read sentence
        2: model return the sentence
        """
        if self.slack_channel.rtm_connect():
            while True:
                self.data = self.slack_channel.rtm_read()
                self.__judge_print()
                time.sleep(1)
        else:
            print("connection Fail")

    def __judge_print(self):
        """
        judge slack call for chainer
        Example:
            chainer:{your sentence}
                chainer return the sentence
            chainer_train:{your sentence}
                start train
        """
        if len(self.data) >= 1 and "text" in self.data[0]:
            print(self.data[0]["text"])
            if "chainer:" in self.data[0]["text"]:
                # input sentence
                src_batch = self.__input_sentence()
                # predict
                hyp_batch = self.__predict_sentence(src_batch)
                # show predict word
                word = ''.join(hyp_batch[0]).replace("</s>", "")
                print(self.slack_channel.api_call("chat.postMessage", user=self.usr, channel=self.chan, text=word))
            if "chainer_train" in self.data[0]["text"]:
                self.__setting_parameter()
                self.__multi_train()

    def __multi_train(self):
        train_path = APP_ROOT + "/../twitter/data/"
        file_list = os.listdir(train_path)
        twitter_source_dict = {}
        twitter_replay_dict = {}
        for file in file_list:
            word_class = re.sub("_replay_twitter_data\.txt|_source_twitter_data\.txt|", file.strip())
            if word_class not in twitter_source_dict:
                twitter_source_dict.update({word_class: file.strip})
            if word_class not in twitter_replay_dict:
                twitter_replay_dict.update({word_class: file.strip})
        for word_class in twitter_source_dict.keys():
            self.parameter["source"] = train_path + twitter_source_dict[word_class]
            self.parameter["target"] = train_path + twitter_replay_dict[word_class]
            self.parameter["model"] = "ChainerDialogue_" + word_class
            model = AttentionDialogue.load_spec(self.parameter["model"] + '.spec', self.XP)
            dialogue = EncoderDecoderModelAttention(self.parameter)
            dialogue.model = self.parameter["model"]
            serializers.load_hdf5(self.parameter["model"] + '.weights', model)
            dialogue.attention_dialogue = model
            dialogue.word2vecFlag = False
            dialogue.train()

    def __input_sentence(self):
        """
        return sentence for chainer predict
        """
        text = self.__mecab_method(self.data[0]["text"].replace("chainer:", ""))
        self.word_class = self.__judge_class(self.data[0]["text"].replace("chainer:", ""))
        data = [text]
        src_batch = [x + ["</s>"] * (self.generation_limit - len(x) + 1) for x in data]
        return src_batch

    def __predict_sentence(self, src_batch):
        """
        predict sentence
        :param src_batch: get the source sentence
        :return:
        """
        dialogue = EncoderDecoderModelAttention(self.parameter)
        src_vocab = Vocabulary.load(self.model_name + '.srcvocab')
        trg_vocab = Vocabulary.load(self.model_name + '.trgvocab')
        model = AttentionDialogue.load_spec(self.model_name + '.spec', self.XP)
        serializers.load_hdf5(self.model_name + '.weights', model)
        hyp_batch = dialogue.forward_implement(src_batch, None, src_vocab, trg_vocab, model, False, self.generation_limit)
        return hyp_batch

    def __setting_parameter(self):
        """
        setteing each patamater
        """
        self.parameter["word2vec"] = self.model_name
        train_path = "../twitter/"
        self.parameter["source"] = train_path + "source_twitter_data.txt"
        self.parameter["target"] = train_path + "replay_twitter_data.txt"

    def __mecab_method(self, text):
        """
        Call the mecab method
        :param text: user input text
        :return:
        """
        mecab_text = self.Mecab.parse(text)
        return mecab_text.split(" ")

    def __judge_class(self, source_txt):
        """
        Judge word class
        :param source_txt(str): twitter source text
        :return: most match class
        """
        class_match_rate = {}
        total_text = self.__mecab_noum_method(source_txt.strip())
        for class_name in self.class_word_vector.keys():
            word_match_count = self.__match_word_count(total_text, class_name)
            if class_name not in class_match_rate:
                class_match_rate.update({class_name: 1.0 * word_match_count / len(self.word_class_dict[class_name])})
        if max(class_match_rate.values()) == 0.0:
            return "other"
        else:
            return max(class_match_rate.items(), key=operator.itemgetter(1))[0]

    def __mecab_noum_method(self, text):
        """
        Call Mecab method split process and choose noum
        :param text:
        :return: only noum
        """
        res = self.Mecab.parseToNode("".join(text))
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
            if word in self.word_class_dict[class_name]:
                word_match_count = word_match_count + 1
        return word_match_count

if __name__ == '__main__':
    data_model = SlackModel()
    data_model.read_config()
    slack = SlackApp(data_model)
    slack.call_method()
