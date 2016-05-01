#'!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3
from chainer import Chain, links, functions


class SrcEmbed(Chain):
  """
  This Class is source word encode the embed id
  """
  def __init__(self, vocab_size, embed_size):
    """
    initial setting
    :param vocab_size:
    :param embed_size:
    """
    super(SrcEmbed, self).__init__(
        source_embed = links.EmbedID(vocab_size, embed_size),
    )

  def __call__(self, source):
    """
    Source to embed space using the tanh
    :param source: source word
    :return:
    """
    return functions.tanh(self.source_embed(source))