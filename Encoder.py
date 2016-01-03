#'!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3

from chainer import Chain, functions, links

class Encoder(Chain):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super(Encoder, self).__init__(
            weight_xi = links.EmbedID(vocab_size, embed_size),
            eh = links.Linear(embed_size, 4 * hidden_size),
            hh = links.Linear(hidden_size, 4 * hidden_size),
        )

    def __call__(self, x, c, h):
        e = functions.tanh(self.weight_xi(x))
        return functions.lstm(c, self.eh(e) + self.hh(h))
