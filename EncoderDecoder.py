#'!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3

from chainer import Chain, functions, links
from Encoder import Encoder
from Decoder import Decoder
import numpy as np
from Common_function import CommonFunction

class EncoderDecoder(Chain):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super(EncoderDecoder, self).__init__(
            enc = Encoder(vocab_size, embed_size, hidden_size),
            dec = Decoder(vocab_size, embed_size, hidden_size),
        )
        self.vocab_size = vocab_size
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.common_function = CommonFunction()

    def reset(self, batch_size):
        self.zerograds()
        self.c = self.common_function.my_zeros((batch_size, self.hidden_size), np.float32)
        self.h = self.common_function.my_zeros((batch_size, self.hidden_size), np.float32)

    def encode(self, x):
        self.c, self.h = self.enc(x, self.c, self.h)

    def decode(self, y):
        y, self.c, self.h = self.dec(y, self.c, self.h)
        return y

    def save_spec(self, filename):
        with open(filename, 'w') as fp:
            print(self.vocab_size, file=fp)
            print(self.embed_size, file=fp)
            print(self.hidden_size, file=fp)

    @staticmethod
    def load_spec(filename):
        with open(filename) as fp:
            vocab_size = int(next(fp))
            embed_size = int(next(fp))
            hidden_size = int(next(fp))
            return EncoderDecoder(vocab_size, embed_size, hidden_size)

