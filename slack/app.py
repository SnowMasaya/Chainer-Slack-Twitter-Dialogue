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
                model = AttentionDialogue.load_spec(self.model_name + '.spec', self.XP)
                dialogue = EncoderDecoderModelAttention(self.parameter)
                serializers.load_hdf5(self.model_name + '.weights', model)
                dialogue.attention_dialogue = model
                dialogue.word2vecFlag = False
                dialogue.train()

    def __input_sentence(self):
        """
        return sentence for chainer predict
        """
        text = self.__mecab_method(self.data[0]["text"].replace("chainer:", ""))
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

if __name__ == '__main__':
    data_model = SlackModel()
    data_model.read_config()
    slack = SlackApp(data_model)
    slack.call_method()
