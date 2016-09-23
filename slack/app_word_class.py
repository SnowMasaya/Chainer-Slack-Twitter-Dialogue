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
from twitter.sqlite_twitter_summary import SqliteTwitterSummary
import pyximport
pyximport.install()
from split_data.input_file_cython import InputFileCython
#QA
from Question_Answer.get_answer import GetAnswer
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))
import re
from execute.execute_dialogue_attention import ExecuteAttentionDialogue


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
        self.model_name = "../model_word_match/ChainerDialogue"
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
        wn_summary_list = APP_ROOT + '/../Data/wn_total_summary_51519_limit05_out_put_list.txt'
        self.input_module = InputFileCython(wn_summary_list)
        self.input_module.input_special_format_file()
        file_list = self.input_module.get_file_data()
        self.class_word_vector = self.__make_class_word_vector(file_list)
        self.sqlite_twitter_summary = SqliteTwitterSummary(self.class_word_vector)
        self.word_class_dict = self.sqlite_twitter_summary.make_class_word_dict()
        self.word_class = ""
        self.multi_train_execute = ExecuteAttentionDialogue()
        self.elastic_search = GetAnswer()

    def __make_class_word_vector(self, file_list):
        """
        Make class word vector dict
        :param file_list:
        :return:
        """
        class_word_vector = {}
        for file in file_list:
            self.input_module = InputFileCython(APP_ROOT + "/../Data/wn_total_summary_51519_limit05_out_put//" + file.strip())
            self.input_module.input_special_format_file()
            if file.strip() not in class_word_vector:
                word_list = (list(map(lambda x:x.strip(), self.input_module.get_file_data())))
                class_word_vector.update({file.strip().replace("_summary.txt", ""): word_list})
        return class_word_vector

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
            input_text = self.data[0]["text"]
            print(input_text)
            if "chainer:" in input_text:
                # predict
                if "?" in input_text or "？" in input_text:
                    replace_input = re.sub("chainer:|\?", "", input_text.strip())
                    self.elastic_search.search_data(replace_input)
                    if len(self.elastic_search.search_result) > 0:
                        hyp_batch = self.elastic_search.search_result[0]
                        print(hyp_batch)
                        if hyp_batch["image"]:
                            word = hyp_batch["image"] + "\n" + hyp_batch["title"] + "\n" + hyp_batch["abstract"] + "\n" + hyp_batch["url"]
                        else:
                            word = hyp_batch["title"] + "\n" + hyp_batch["abstract"] + "\n" + hyp_batch["url"]
                    else:
                        word = "No match"
                else:
                    # input sentence
                    src_batch = self.__input_sentence()
                    hyp_batch = self.__predict_sentence(src_batch)
                    word = ''.join(hyp_batch[0]).replace("</s>", "")
                # show predict word
                print(self.slack_channel.api_call("chat.postMessage", user=self.usr, channel=self.chan, text=word))
            if "chainer_train" in self.data[0]["text"]:
                self.__setting_parameter()
                self.__multi_train()

    def __multi_train(self):
        """
        Call multi train
        """
        self.multi_train_execute.train_mulit_model()

    def __input_sentence(self):
        """
        return sentence for chainer predict
        """
        text = self.__mecab_method(self.data[0]["text"].replace("chainer:", ""))
        self.word_class = self.sqlite_twitter_summary.judge_class(self.data[0]["text"].replace("chainer:", ""))
        ##  self.word_class = self.sqlite_twitter_summary.judge_class_wiki_vector(self.data[0]["text"].replace("chainer:", ""))
        data = [text]
        src_batch = [x + ["</s>"] * (self.generation_limit - len(x) + 1) for x in data]
        return src_batch

    def __predict_sentence(self, src_batch):
        """
        predict sentence
        :param src_batch: get the source sentence
        :return:
        """
        self.model_name = "../model_word_match/ChainerDialogue_" + self.word_class
        print(self.word_class)
        dialogue = EncoderDecoderModelAttention(self.parameter)
        src_vocab = Vocabulary.load(self.model_name + '.srcvocab')
        trg_vocab = Vocabulary.load(self.model_name + '.trgvocab')
        model = AttentionDialogue.load_spec(self.model_name + '.spec', self.XP)
        serializers.load_hdf5(self.model_name + '.weights', model)
        hyp_batch = dialogue.forward_implement(src_batch, None, src_vocab, trg_vocab, model, False, self.generation_limit)
        print(hyp_batch)
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

if __name__ == '__main__':
    data_model = SlackModel()
    data_model.read_config()
    slack = SlackApp(data_model)
    slack.call_method()
