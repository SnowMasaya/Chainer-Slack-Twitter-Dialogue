#'!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3

from chainer import Chain, functions, links


class AttentionEncoder(Chain):
    """
    Attention Encoder
        Setting only embed size and hidden size.
        Remove the Vocabuary size because SrcEmbed class is the source to embed
    """
    def __init__(self, embed_size, hidden_size):
        """
        :param embed_size:
        :param hidden_size:
        :return:
        """
        super(AttentionEncoder, self).__init__(
            source_to_hidden = links.Linear(embed_size, 4 * hidden_size),
            hidden_to_hidden = links.Linear(hidden_size, 4 * hidden_size),
        )

    def __call__(self, source, current, hidden):
        """
        Call Only LSTM
        :param source:
        :param current: setting the current value
        :param hidden:
        :return:
        """
        return functions.lstm(current, self.source_to_hidden(source) + self.hidden_to_hidden(hidden))
