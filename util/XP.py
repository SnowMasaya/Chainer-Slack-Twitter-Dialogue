# '!/usr/bin/env python
# -*- coding:utf-8 -*-
# !/usr/bin/python3
from chainer import cuda, Variable
import numpy


class XP:
    """
    Excahnge Variable for gpu
    all method is the static function because setting gpu or cpu in the one time
    """
    __lib = None

    @staticmethod
    def set_library(use_gpu, gpu_id):
        """
        You choose the gpu
        :param use_gpu: setting boolean value for using the gpu
        :param gpu_id: setting gpu id
        """
        if use_gpu:
            XP.__lib = cuda.cupy
            cuda.get_device(gpu_id).use()
        else:
            XP.__lib = numpy

    @staticmethod
    def __zeros(shape, dtype):
        """
        change the zero velue
        :param shape:
        :param dtype: gpu or cpu
        """
        return Variable(XP.__lib.zeros(shape, dtype=dtype))

    @staticmethod
    def fzeros(shape):
        """
        call change the zero velue function
        :param shape:
        """
        return XP.__zeros(shape, XP.__lib.float32)

    @staticmethod
    def __array(array, dtype):
        """
        change the array velue
        :param array:
        :param dtype: gpu or cpu
        """
        return Variable(XP.__lib.array(array, dtype=dtype))

    @staticmethod
    def iarray(array):
        """
        change the int array velue
        we parepare the two function for int and float because it is different data type
        :param array: change the value
        """
        return XP.__array(array, XP.__lib.int32)

    @staticmethod
    def farray(array):
        """
        change the float array velue
        :param array: change the value
        """
        return XP.__array(array, XP.__lib.float32)
