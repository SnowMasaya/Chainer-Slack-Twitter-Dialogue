# '!/usr/bin/env python
# -*- coding:utf-8 -*-
# !/usr/bin/python3
from chainer import Chain
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from attention import Attention
from src_embed import SrcEmbed
sys.path.append(os.path.join(os.path.dirname(__file__), "../."))
from attention_encoder import AttentionEncoder
from attention_decoder import AttentionDecoder


class AttentionDialogue(Chain):
    """
    Atteition Dialogue
    """
    def __init__(self, vocab_size, embed_size, hidden_size, XP):
        """
        initial setting
        :param vocab_size:
        :param embed_size:
        :param hidden_size:
        :return:
        """
        super(AttentionDialogue, self).__init__(
            emb=SrcEmbed(vocab_size, embed_size),
            forward_encode=AttentionEncoder(embed_size, hidden_size),
            back_encdode=AttentionEncoder(embed_size, hidden_size),
            attention=Attention(hidden_size),
            dec=AttentionDecoder(vocab_size, embed_size, hidden_size),
        )
        self.vocab_size = vocab_size
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.XP = XP

    def reset(self):
        """
        initial setting value
        """
        self.zerograds()
        self.source_list = []

    def embed(self, source):
        """
        source change to embed
        """
        self.source_list.append(self.emb(source))

    def encode(self):
        """
        encode the source into the attention space
        """
        batch_size = self.source_list[0].data.shape[0]
        ZEROS = self.XP.fzeros((batch_size, self.hidden_size))
        context = ZEROS
        annotion = ZEROS
        annotion_list = []
        # Get the annotion list
        for source in self.source_list:
            context, annotion = self.forward_encode(source, context, annotion)
            annotion_list.append(annotion)
        context = ZEROS
        back_word = ZEROS
        back_word_list = []
        # Get the back word list
        for source in reversed(self.source_list):
            context, back_word = self.back_encdode(source, context, back_word)
            back_word_list.insert(0, back_word)
        self.annotion_list = annotion_list
        self.back_word_list = back_word_list
        self.context = ZEROS
        self.hidden = ZEROS

    def decode(self, target_word):
        """
        decode the target word
        """
        annotion_value, back_word_value = self.attention(self.annotion_list, self.back_word_list, self.hidden)
        target_word, self.context, self.hidden = self.dec(target_word, self.context, self.hidden, annotion_value, back_word_value)
        return target_word

    def save_spec(self, filename):
        """
        Separate save because it is easy to change the each load spec
        """
        with open(filename, 'w') as fp:
            print(self.vocab_size, file=fp)
            print(self.embed_size, file=fp)
            print(self.hidden_size, file=fp)

    @staticmethod
    def load_spec(filename, XP):
        """
        Separate load because it is easy to change the each load spec
        """
        with open(filename) as fp:
            vocab_size = int(next(fp))
            embed_size = int(next(fp))
            hidden_size = int(next(fp))
            return AttentionDialogue(vocab_size, embed_size, hidden_size, XP)
