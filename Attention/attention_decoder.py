# '!/usr/bin/env python
# -*- coding:utf-8 -*-
# !/usr/bin/python3

from chainer import Chain, functions, links


class AttentionDecoder(Chain):
    """
    Need The More hidden function for annotation and back word
    """

    def __init__(self, vocab_size, embed_size, hidden_size):
        """
        Add the hidden layer annotation and back word
        :param vocab_size:
        :param embed_size:
        :param hidden_size:
        :return:
        """
        super(AttentionDecoder, self).__init__(
            embed_vocab=links.EmbedID(vocab_size, embed_size),
            embed_hidden=links.Linear(embed_size, 4 * hidden_size),
            hidden_hidden=links.Linear(hidden_size, 4 * hidden_size),
            annotation_hidden=links.Linear(embed_size, 4 * hidden_size),
            back_word_hidden=links.Linear(hidden_size, 4 * hidden_size),
            hidden_embed=links.Linear(hidden_size, embed_size),
            embded_target=links.Linear(embed_size, vocab_size),
        )

    def __call__(self, target, current, hidden, annotation, back_word):
        """
        Attention Decoder
        :param target(list): target word list
        :param current: current weight
        :param hidden: hidden weight
        :param annotation: annotation_weight
        :param back_word: back_word weight
        :return:
        """
        embed = functions.tanh(self.embed_vocab(target))
        current, hidden = functions.lstm(current, self.embed_hidden(embed) + self.hidden_hidden(hidden) +
                                         self.annotation_hidden(annotation) + self.back_word_hidden(back_word))
        embed_hidden = functions.tanh(self.hidden_embed(hidden))
        return self.embded_target(embed_hidden), current, hidden
