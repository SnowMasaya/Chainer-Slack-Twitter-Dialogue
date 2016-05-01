#'!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3
#表示用に使用しています。
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from util.functions import trace
import numpy as np

from chainer import Chain, Variable, cuda, functions, links, optimizer, optimizers, serializers

from EncoderDecoderModelAttention import EncoderDecoderModelAttention

from word2vec.word2vec_load import SkipGram,SoftmaxCrossEntropyLoss

unit = 300
vocab = 5000
loss_func = SoftmaxCrossEntropyLoss(unit, vocab)
w2v_model = SkipGram(vocab, unit, loss_func)
serializers.load_hdf5("./../word2vec/word2vec_chainer.model", w2v_model)

parameter_dict = {}
train_path = "../Data/"
parameter_dict["source"] = train_path + "player_1_wakati"
parameter_dict["target"] = train_path + "player_2_wakati"
parameter_dict["test_source"] = train_path + "player_1_wakati"
parameter_dict["test_target"] = train_path + "player_2_test"

"""
下記の値が大きいほど扱える語彙の数が増えて表現力が上がるが計算量が爆発的に増えるので大きくしない方が良いです。
"""
parameter_dict["vocab"] = 5000

"""
この数が多くなればなるほどモデルが複雑になります。この数を多くすると必然的に学習回数を多くしないと学習は
収束しません。
語彙数よりユニット数の数が多いと潜在空間への写像が出来ていないことになり結果的に意味がない処理になります。
"""
parameter_dict["embed"] = 300

"""
この数も多くなればなるほどモデルが複雑になります。この数を多くすると必然的に学習回数を多くしないと学習は
収束しません。
"""
parameter_dict["hidden"] = 300

"""
学習回数。基本的に大きい方が良いが大きすぎると収束しないです。
"""
parameter_dict["epoch"] = 20

"""
ミニバッチ学習で扱うサイズです。この点は経験的に調整する場合が多いが、基本的に大きくすると学習精度が向上する
代わりに学習スピードが落ち、小さくすると学習精度が低下する代わりに学習スピードが早くなります。
"""
parameter_dict["minibatch"] = 100

"""
予測の際に必要な単語数の設定。長いほど多くの単語の翻訳が確認できるが、一般的にニューラル翻訳は長い翻訳には
向いていないので小さい数値がオススメです。
"""
parameter_dict["generation_limit"] = 256

parameter_dict["word2vec"] = w2v_model

parameter_dict["word2vecFlag"] = False


parameter_dict["attention_dialogue"] = ""

trace('initializing ...')

encoderDecoderModel = EncoderDecoderModelAttention(parameter_dict)
encoderDecoderModel.train()

model_name = "ChainerDialogue.021"
trace('initializing ...')

encoderDecoderModel = EncoderDecoderModelAttention(parameter_dict)
encoderDecoderModel.test()