#'!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from chainer import Chain, Variable, cuda, functions, links, optimizer, optimizers, serializers
from chainer import link

import util.generators as gens
from util.functions import trace, fill_batch
from util.vocabulary import Vocabulary
from Attention.attention_dialogue import AttentionDialogue
import random
from util.XP import XP
from os import path
APP_ROOT = path.dirname(path.abspath(__file__))


class EncoderDecoderModelAttention:

    def __init__(self, parameter_dict):
        """
        Initial Paramater Setting
        :param parameter_dict: setting the a varity of paramater
        If you use gpu, you setting the bellow paramater
            XP.set_library(True, {your gpu id})
        """
        self.parameter_dict       = parameter_dict
        self.source               = parameter_dict["source"]
        self.target               = parameter_dict["target"]
        self.test_source          = parameter_dict["test_source"]
        self.test_target          = parameter_dict["test_target"]
        self.vocab                = parameter_dict["vocab"]
        self.embed                = parameter_dict["embed"]
        self.hidden               = parameter_dict["hidden"]
        self.epoch                = parameter_dict["epoch"]
        self.minibatch            = parameter_dict["minibatch"]
        self.generation_limit     = parameter_dict["generation_limit"]
        self.word2vec = parameter_dict["word2vec"]
        self.word2vecFlag = parameter_dict["word2vecFlag"]
        self.model = parameter_dict["model"]
        self.attention_dialogue   = parameter_dict["attention_dialogue"]
        XP.set_library(False, 0)
        self.XP = XP

    def forward(self, src_batch, trg_batch, src_vocab, trg_vocab, attention, is_training, generation_limit):
        pass

    def forward_implement(self, src_batch, trg_batch, src_vocab, trg_vocab, attention, is_training, generation_limit):
        """
        chainer forward method
        :param src_batch(lise): source_sentence
        :param trg_batch(lise):
        :param src_vocab:
        :param trg_vocab:
        :param attention:
        :param is_training(boolean): setting the traing flag
        :param generation_limit(int): useing method for predict
        :return:
        """
        batch_size = len(src_batch)
        src_len = len(src_batch[0])
        trg_len = len(trg_batch[0]) if trg_batch else 0
        src_stoi = src_vocab.stoi
        trg_stoi = trg_vocab.stoi
        trg_itos = trg_vocab.itos
        attention.reset()

        x = self.XP.iarray([src_stoi('</s>') for _ in range(batch_size)])
        attention.embed(x)
        for l in reversed(range(src_len)):
            x = self.XP.iarray([src_stoi(src_batch[k][l]) for k in range(batch_size)])
            attention.embed(x)

        attention.encode()

        t = self.XP.iarray([trg_stoi('<s>') for _ in range(batch_size)])
        hyp_batch = [[] for _ in range(batch_size)]

        if is_training:
            loss = self.XP.fzeros(())
            for l in range(trg_len):
                y = attention.decode(t)
                t = self.XP.iarray([trg_stoi(trg_batch[k][l]) for k in range(batch_size)])
                loss += functions.softmax_cross_entropy(y, t)
                output = cuda.to_cpu(y.data.argmax(1))
                for k in range(batch_size):
                    hyp_batch[k].append(trg_itos(output[k]))
            return hyp_batch, loss

        else:
            while len(hyp_batch[0]) < generation_limit:
                y = attention.decode(t)
                output = cuda.to_cpu(y.data.argmax(1))
                t = self.XP.iarray(output)
                for k in range(batch_size):
                    hyp_batch[k].append(trg_itos(output[k]))
                if all(hyp_batch[k][-1] == '</s>' for k in range(batch_size)):
                    break

        return hyp_batch

    def train(self):
        """
        Train method
        If you use the word2vec model, you possible to use the copy weight
        Optimizer method use the Adagrad
        """
        trace('making vocabularies ...')
        src_vocab = Vocabulary.new(gens.word_list(self.source), self.vocab)
        trg_vocab = Vocabulary.new(gens.word_list(self.target), self.vocab)

        trace('making model ...')
        self.attention_dialogue = AttentionDialogue(self.vocab, self.embed, self.hidden, self.XP)
        if self.word2vecFlag:
            self.copy_model(self.word2vec, self.attention_dialogue.emb)
            self.copy_model(self.word2vec, self.attention_dialogue.dec, dec_flag=True)

        for epoch in range(self.epoch):
            trace('epoch %d/%d: ' % (epoch + 1, self.epoch))
            trained = 0
            gen1 = gens.word_list(self.source)
            gen2 = gens.word_list(self.target)
            gen3 = gens.batch(gens.sorted_parallel(gen1, gen2, 100 * self.minibatch), self.minibatch)
            opt = optimizers.AdaGrad(lr = 0.01)
            opt.setup(self.attention_dialogue)
            opt.add_hook(optimizer.GradientClipping(5))

            random_number = random.randint(0, self.minibatch - 1)
            for src_batch, trg_batch in gen3:
                src_batch = fill_batch(src_batch)
                trg_batch = fill_batch(trg_batch)
                K = len(src_batch)
                hyp_batch, loss = self.forward_implement(src_batch, trg_batch, src_vocab, trg_vocab, self.attention_dialogue, True, 0)
                loss.backward()
                opt.update()

                self.print_out(random_number, epoch, trained, src_batch, trg_batch, hyp_batch)

                trained += K

        trace('saving model ...')
        prefix = self.model
        model_path = APP_ROOT + "/model/" + prefix
        src_vocab.save(model_path + '.srcvocab')
        trg_vocab.save(model_path + '.trgvocab')
        self.attention_dialogue.save_spec(model_path + '.spec')
        serializers.save_hdf5(model_path + '.weights', self.attention_dialogue)

        trace('finished.')

    def test(self):
        """
        Test method
        You have to parepare the train model
        """
        trace('loading model ...')
        prefix = self.model
        model_path = APP_ROOT + "/model/" + prefix
        src_vocab = Vocabulary.load(model_path + '.srcvocab')
        trg_vocab = Vocabulary.load(model_path + '.trgvocab')
        self.attention_dialogue = AttentionDialogue.load_spec(model_path + '.spec', self.XP)
        serializers.load_hdf5(model_path + '.weights', self.attention_dialogue)

        trace('generating translation ...')
        generated = 0

        with open(self.test_target, 'w') as fp:
            for src_batch in gens.batch(gens.word_list(self.source), self.minibatch):
                src_batch = fill_batch(src_batch)
                K = len(src_batch)

                trace('sample %8d - %8d ...' % (generated + 1, generated + K))
                hyp_batch = self.forward_implement(src_batch, None, src_vocab, trg_vocab, self.attention_dialogue, False, self.generation_limit)

                source_cuont = 0
                for hyp in hyp_batch:
                    hyp.append('</s>')
                    hyp = hyp[:hyp.index('</s>')]
                    print("src : " + "".join(src_batch[source_cuont]).replace("</s>", ""))
                    print('hyp : ' +''.join(hyp))
                    print(' '.join(hyp), file=fp)
                    source_cuont = source_cuont + 1

                generated += K

        trace('finished.')

    def print_out(self, K, i_epoch, trained, src_batch, trg_batch, hyp_batch):
        """
        Print out
        :param K:
        :param i_epoch:
        :param trained: train times
        :param src_batch:
        :param trg_batch:
        :param hyp_batch:
        :return:
        """
        if K > len(src_batch) and K > len(trg_batch) and K > len(hyp_batch):
            K = len(src_batch) - 1

        trace('epoch %3d/%3d, sample %8d' % (i_epoch + 1, self.epoch, trained + K + 1))
        trace('  src = ' + ' '.join([x if x != '</s>' else '*' for x in src_batch[K]]))
        trace('  trg = ' + ' '.join([x if x != '</s>' else '*' for x in trg_batch[K]]))
        trace('  hyp = ' + ' '.join([x if x != '</s>' else '*' for x in hyp_batch[K]]))


    def copy_model(self, src, dst, dec_flag=False):
        """
        Weight Copyt method
        :param src: Word2Vec Model
        :param dst: Dialogue Model
        :param dec_flag: Decoder flag
        :return:
        """
        print("start copy")
        for child in src.children():
            if dec_flag:
                if dst["embded_target"] and child.name == "weight_xi" and self.word2vecFlag:
                    for a, b in zip(child.namedparams(), dst["embded_target"].namedparams()):
                        b[1].data = a[1].data
                    print('Copy weight_jy')
            if child.name not in dst.__dict__: continue
            dst_child = dst[child.name]
            if type(child) != type(dst_child): continue
            if isinstance(child, link.Chain):
                self.copy_model(child, dst_child)
            if isinstance(child, link.Link):
                match = True
                for a, b in zip(child.namedparams(), dst_child.namedparams()):
                    if a[0] != b[0]:
                        match = False
                        break
                    if a[1].data.shape != b[1].data.shape:
                        match = False
                        break
                if not match:
                    print('Ignore %s because of parameter mismatch' % child.name)
                    continue
                for a, b in zip(child.namedparams(), dst_child.namedparams()):
                    b[1].data = a[1].data
                print('Copy %s' % child.name)
