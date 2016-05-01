#!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3
"""Sample script of word embedding model.
This code implements skip-gram model and continuous-bow model.
Use ../ptb/download.py to download 'ptb.train.txt'.
"""
import argparse
import collections
import time

import numpy as np

import chainer
from chainer import cuda
import chainer.functions as F
import chainer.links as L
import chainer.optimizers as O
import pyximport
pyximport.install()
from adam import Adam
from variable import Variable
from chainer import serializers

args = {}
args["data"]= "../Data/jawiki-latest-random-titles-in-ns0"
args['unit'] = 300
args['window'] = 5
args['batchsize'] = 100
args['epoch'] = 10
#model type (skipgram, cbow)
args['model'] = 'skipgram'
#choices=['hsm', 'ns', 'original']
args['out_type'] = 'original'

xp = np

print("# unit: {}".format(args["unit"]))
print("Window : {}".format(args["window"]))
print("Minibatch-size: {}".format(args["batchsize"]))
print("# epoch: {}".format(args["epoch"]))
print("Traing model: {}".format(args["model"]))
print("Output type: {}".format(args["out_type"]))

class ContinuousBow(chainer.Chain):

    def __init__(self, n_vocab, n_units, loo_func):
        super(ContinuousBow, self).__init__(
            weight_xi = F.EmbedID(n_vocab, args["unit"]),
            loss_func = loo_func,
        )

    def __call__(self, x, context):
        h = None
        for c in context:
            e = self.weight_xi(c)
            h = h + e if h is not None else e

        return self.loss_func(h, x)

class SkipGram(chainer.Chain):

    def __init__(self, n_vocab, n_units, loss_func):
        super(SkipGram, self).__init__(
            weight_xi = L.EmbedID(n_vocab, n_units),
            loss_func = loss_func
        )

    def __call__(self, x, context):
        loss = None
        for c in context:
            e = self.weight_xi(c)

            loss_i = self.loss_func(e, x)
            loss = loss_i if loss is None else loss + loss_i

        return loss

class SoftmaxCrossEntropyLoss(chainer.Chain):
    def __init__(self, n_in, n_out):
        super(SoftmaxCrossEntropyLoss, self).__init__(
            W=L.Linear(n_in, n_out)
        )
    def __call__(self, x, t):
        return F.softmax_cross_entropy(self.W(x), t)

cdef calculate_loss(model, dataset, position):
    w = np.random.randint(args["window"] - 1 ) + 1
    context = []
    for offset in range(-w, w + 1):
        if offset == 0:
            continue
        c_data = xp.asarray(dataset[position + offset])
        c = Variable(c_data)
        context.append(c)
    x_data = xp.asanyarray(dataset[position])
    x = Variable(x_data)
    return model(x, context)

cdef:
    dict index2word = {}
    dict word2index = {}

counts = collections.Counter()

cdef execute_c():
    dataset = []
    with open(args["data"]) as f:
        for line in f:
            for word in line.split():
                if word not in word2index:
                   ind = len(word2index)
                   word2index[word] = ind
                   index2word[ind] = word
                counts[word2index[word]] += 1
                dataset.append(word2index[word])

    n_vocab = len(word2index)

    print("n_vocab: %d" % n_vocab)
    print("data length: %d" % len(dataset))

    if args["out_type"] == "hsm":
        HSM = L.BinaryHierarchicalSoftmax
        tree = HSM.create_huffman_tree(counts)
        loss_func = HSM(args["unit"], tree)
    elif args["out_type"] == "ns":
        cs = [counts[w] for w in range(len(counts))]
        loss_func = L.NegativeSampling(args["unit"], cs, 20)
    elif args["out_type"] == "original":
        loss_func = SoftmaxCrossEntropyLoss(args["unit"], n_vocab)
    else:
        raise Exception("Unknown output type: {}".format(args["out_type"]))

    if args["model"] == "skipgram":
        model = SkipGram(n_vocab, args["unit"], loss_func)
    elif args["model"] == "cbow":
        model = ContinuousBow(n_vocab, args["unit"], loss_func)
    else:
        raise Exception('Unknown model type:'.format(args["model"]))

    dataset = np.array(dataset, dtype=np.int32)

    optimizer = Adam()
    optimizer.setup(model)

    begin_time = time.time()
    cur_at = begin_time
    word_count = 0
    skip = (len(dataset) - args["window"] * 2) // args["batchsize"]
    next_count = 100000
    for epoch in range(args["epoch"]):
        accum_loss = 0
        print('epoch: {0}'.format(epoch))
        indexes = np.random.permutation(skip)
        for i in indexes:
            if word_count >= next_count:
                now = time.time()
                duration = now - cur_at
                throuput = 100000. / duration
                print('{} word, {:.2f} sec, {:.2f} word/sec'.format(
                    word_count, duration, throuput)
                )
                next_count += 100000
                cur_at = now

            position = np.array(
                range(0, args["batchsize"])) * skip + (args["window"] + i)
            loss = calculate_loss(model, dataset, position)
            accum_loss += loss.data
            word_count += args["batchsize"]

            model.zerograds()
            loss.backward()
            optimizer.update()

        serializers.save_hdf5("word2vec_chainer.model", model)
        print(accum_loss)

    with open('word2vec.model', 'w') as f:
        f.write('%d %d\n' % (len(index2word), args["unit"]))
        w = model.weight_xi.W.data
        for i in range(w.shape[0]):
            v =  ' '.join(['%f' % v for v in w[i]])
            f.write('%s %s\n' % (index2word[i], v))

def execute():
    execute_c()

