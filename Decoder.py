#'!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3

from chainer import Chain, functions, links

class Decoder(Chain):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super(Decoder, self).__init__(
            ye = links.EmbedID(vocab_size, embed_size),
            eh = links.Linear(embed_size, 4 * hidden_size),
            hh = links.Linear(hidden_size, 4 * hidden_size),
            hf = links.Linear(hidden_size, embed_size),
            weight_jy = links.Linear(embed_size, vocab_size),
        )

    def __call__(self, y, c, h):
        e = functions.tanh(self.ye(y))
        c, h = functions.lstm(c, self.eh(e) + self.hh(h))
        f = functions.tanh(self.hf(h))
        return self.weight_jy(f), c, h
