# '!/usr/bin/env python
# -*- coding:utf-8 -*-
# !/usr/bin/python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from util.XP import XP
from chainer import Chain, links, functions


class Attention(Chain):
    """
    Attention Model
        Attention mechanism weight_exponentialno longer try encode the full source sentence into a fixed length vector.
        Rather, weight_exponentialallow the decoder to "attend" to different parts pf the source sentence at each step of the output
        generation
    Reference
        article:
            http://www.wildml.com/2016/01/annotion-and-memory-in-deep-learning-and-nlp/
        paper:
            http://arxiv.org/pdf/1409.0473v6.pdf
        code:
            https://github.com/odashi/chainer_examples/blob/master/chainer-1.5/mt_s2s_annotion.py
    """
    def __init__(self, hidden_size):
        """
        Initial setting the Attention model
        :param hidden_size:
        :return:
        """
        super(Attention, self).__init__(
            annotion_weight=links.Linear(hidden_size, hidden_size),
            back_weight=links.Linear(hidden_size, hidden_size),
            pw=links.Linear(hidden_size, hidden_size),
            weight_exponential=links.Linear(hidden_size, 1),
        )
        self.hidden_size = hidden_size

    def __call__(self, annotion_list, back_word_list, p):
        """
        Calculate the annotion and back word value
        :param annotion_list:
        :param back_word_list:
        :param p: hidden value
        :return:
        """
        batch_size = p.data.shape[0]
        exponential_list = []
        sum_exponential = XP.fzeros((batch_size, 1))
        # Calculate the total value list and total value
        # Prepare the Convoluation
        for annotion, back_word in zip(annotion_list, back_word_list):
            weight = functions.tanh(self.annotion_weight(annotion) + self.back_weight(back_word) + self.pw(p))
            exponential = functions.exp(self.weight_exponential(weight))
            exponential_list.append(exponential)
            sum_exponential += exponential
        ZEROS = XP.fzeros((batch_size, self.hidden_size))
        annotion_value = ZEROS
        back_word_value = ZEROS
        # Calculate the Convolution Value each annotion and back word
        for annotion, back_word, exponential in zip(annotion_list, back_word_list, exponential_list):
            exponential /= sum_exponential
            annotion_value += functions.reshape(functions.batch_matmul(annotion, exponential), (batch_size, self.hidden_size))
            back_word_value += functions.reshape(functions.batch_matmul(back_word, exponential), (batch_size, self.hidden_size))
        return annotion_value, back_word_value
