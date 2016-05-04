# '!/usr/bin/env python
# -*- coding:utf-8 -*-
# !/usr/bin/python3
# 表示用に使用しています。
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from util.functions import trace
from chainer import serializers
from EncoderDecoderModel import EncoderDecoderModel
from word2vec.word2vec_load import SkipGram, SoftmaxCrossEntropyLoss


class ExecuteDialogue(object):
    """
    Execute Dialogue Class
    """
    def __init__(self):
        """
        Iniitial Setting
        Setting Word2Vec
        Seeting Dialogue Paramater
        If you use word2vec you have to care the each paramater
            you set the same size Word2vec
            self.parameter_dict["vocab"]
            self.parameter_dict["embed"]
            You setting the word2vec model
            self.parameter_dict["word2vec"] = w2v_model
            self.parameter_dict["word2vecFlag"] = True
        """
        # Seeting Word2Vec
        unit = 300
        vocab = 5000
        loss_func = SoftmaxCrossEntropyLoss(unit, vocab)
        w2v_model = SkipGram(vocab, unit, loss_func)
        serializers.load_hdf5("./../word2vec/word2vec_chainer.model", w2v_model)

        # Setting Dilogue Paramater
        self.parameter_dict = {}
        train_path = "../Data/"
        self.parameter_dict["source"] = train_path + "player_1_wakati"
        self.parameter_dict["target"] = train_path + "player_2_wakati"
        self.parameter_dict["test_source"] = train_path + "player_1_wakati"
        self.parameter_dict["test_target"] = train_path + "player_2_test"

        """
        下記の値が大きいほど扱える語彙の数が増えて表現力が上がるが計算量が爆発的に増えるので大きくしない方が良いです。
        """
        self.parameter_dict["vocab"] = 5000

        """
        この数が多くなればなるほどモデルが複雑になります。この数を多くすると必然的に学習回数を多くしないと学習は
        収束しません。
        語彙数よりユニット数の数が多いと潜在空間への写像が出来ていないことになり結果的に意味がない処理になります。
        """
        self.parameter_dict["embed"] = 300

        """
        この数も多くなればなるほどモデルが複雑になります。この数を多くすると必然的に学習回数を多くしないと学習は
        収束しません
        """
        self.parameter_dict["hidden"] = 200

        """
        学習回数。基本的に大きい方が良いが大きすぎると収束しないです。
        """
        self.parameter_dict["epoch"] = 20

        """
        ミニバッチ学習で扱うサイズです。この点は経験的に調整する場合が多いが、基本的に大きくすると学習精度が向上する
        代わりに学習スピードが落ち、小さくすると学習精度が低下する代わりに学習スピードが早くなります。
        """
        self.parameter_dict["minibatch"] = 64

        """
        予測の際に必要な単語数の設定。長いほど多くの単語の翻訳が確認できるが、一般的にニューラル翻訳は長い翻訳には
        向いていないので小さい数値がオススメです。
        """
        self.parameter_dict["generation_limit"] = 256

        self.parameter_dict["word2vec"] = w2v_model

        self.parameter_dict["word2vecFlag"] = True

        self.parameter_dict["encdec"] = ""

    def train(self):
        """
        Call the Dialogue Training
        """
        trace('initializing ...')

        encoderDecoderModel = EncoderDecoderModel(self.parameter_dict)
        encoderDecoderModel.train()

    def test(self):
        """
        Call the Dialogue Test
        """
        trace('initializing ...')

        encoderDecoderModel = EncoderDecoderModel(self.parameter_dict)
        encoderDecoderModel.test()

if __name__ == '__main__':
    execute_dialogue = ExecuteDialogue()
    execute_dialogue.train()
    execute_dialogue.test()
