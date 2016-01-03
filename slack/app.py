import time
from slackclient import SlackClient
import yaml
from collections import namedtuple
from slack_model import SlackModel
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from chainer_slack.EncoderDecoderModelForwardSlack import EncoderDecoderModelForwardSlack
from EncoderDecoder import EncoderDecoder

from chainer import serializers
import numpy
import util.generators as gens
from util.functions import trace, fill_batch
from util.vocabulary import Vocabulary
import MeCab

class SlackApp():

    def __init__(self, data_model):
        self.sc          = data_model.sc
        self.data = ""
        self.parameter = data_model.parameter_dict
        self.model_name = "../ChainerDialogue"
        self.generation_limit = 200
        """
        We confirm channel number
        https://api.slack.com/methods/channels.list
        """
        self.chan = data_model.chan
        self.usr  = data_model.user
        self.mecab_dict  = data_model.mecab_dict
        self.Mecab = MeCab.Tagger("-Owakati -d %s" % self.mecab_dict)

    def call_method(self):
        if self.sc.rtm_connect():
            while True:
                self.data = self.sc.rtm_read()
                self.__judge_print()
                time.sleep(1)
        else:
            print("connection Fail")

    def __judge_print(self):
        if len(self.data) >= 1 and "text" in self.data[0]:
            print(self.data[0]["text"])
            if "chainer:" in self.data[0]["text"]:
                # input sentence
                src_batch = self.__input_sentence()
                #predict
                hyp_batch = self.__predict_sentence(src_batch)
                #show predict word
                word = ''.join(hyp_batch[0]).replace("</s>", "")
                print(self.sc.api_call("chat.postMessage", user=self.usr, channel = self.chan, text = word))
            if "chainer_train" in self.data[0]["text"]:
                self.__setting_parameter()
                model = EncoderDecoder.load_spec(self.model_name + '.spec')
                dialogue = EncoderDecoderModelForwardSlack(self.parameter)
                serializers.load_hdf5(dialogue.model + '.weights', model)
                dialogue.encdec = model
                dialogue.word2vecFlag = False
                dialogue.train()

    def __input_sentence(self):
        text = self.__mecab_method(self.data[0]["text"].replace("chainer:", ""))
        data = [text]
        src_batch = [x + ["</s>"] * (self.generation_limit - len(x) + 1) for x in data]
        return src_batch

    def __predict_sentence(self, src_batch):
        dialogue = EncoderDecoderModelForwardSlack(self.parameter)
        src_vocab = Vocabulary.load(self.model_name + '.srcvocab')
        trg_vocab = Vocabulary.load(self.model_name + '.trgvocab')
        model = EncoderDecoder.load_spec(self.model_name + '.spec')
        serializers.load_hdf5(dialogue.model + '.weights', model)
        hyp_batch = dialogue.forward(src_batch, None, src_vocab, trg_vocab, model, False, self.generation_limit)
        return hyp_batch

    def __setting_parameter(self):
        self.parameter["word2vec"] = self.model_name
        train_path = "../twitter/"
        self.parameter["source"]   = train_path + "source_twitter_data.txt"
        self.parameter["target"]   = train_path + "replay_twitter_data.txt"


    def __mecab_method(self, text):
        mecab_text = self.Mecab.parse(text)
        return mecab_text.split(" ")

if __name__ == '__main__':
    data_model = SlackModel()
    data_model.read_config()
    slack = SlackApp(data_model)
    slack.call_method()
