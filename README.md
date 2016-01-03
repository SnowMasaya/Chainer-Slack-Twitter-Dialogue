Chainer Dialogue
====

This tool is making Dialogue Model


## Description
This tool is making the Dialogue Model

If you see the detail about it, you see the below<br> 
#
### Install

If you don't install pyenv and virtualenv you have to install bellow
####Prepare Install
linux
```
apt-get install pyenv 
apt-get install virtualenv 
```
Mac
```
brew install pyenv 
brew install virtualenv 
```

####Prepare Inastall2
```
pyenv install 3.4.1
pyenv rehash
pyenv local 3.4.1
virtualenv -p ~/.pyenv/versions/3.4.1/bin/python3.4 my_env
source my_env/bin/activate

```

```
pip install -r requirement.txt 
```
Installing a library bellow
##Requirements

    Python 3.4+
    numpy
    chainer
    ipython
    notebook
    jinja2
    pyzmq
    tornado

####Confirm library

```
ipython
```

Type command bellow
```
import math
import sys
import time

import numpy as np
import six

import chainer
from chainer import cuda
import chainer.functions as F
from chainer import optimizers
```

#
### Usage 
#
```
*You execute python 
ipython notebook
```
#
### Data Directory Structure 
#
```
samples/　　　　　... Sample model and Translation result
  - middle/ 　　　　　... middle setteing
train/　     　... training data set
test/ 　　　　　　　... test data set
```
#
### Licence
#
```
The MIT License (MIT)

Copyright (c) 2015 Masaya Ogushi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
#
### Author
#
[SnowMasaya](https://github.com/SnowMasaya)
### References 
#
>[Chainer]http://chainer.org/<br>
>[Python Slack]https://github.com/slackhq/python-slackclient<br>
>[Chainer Machine Translation]https://github.com/odashi/chainer_examples<br>
>[Dialogue Data]https://sites.google.com/site/dialoguebreakdowndetection/<br>
>[Chainer Word2Vec]https://github.com/pfnet/chainer/blob/master/examples/word2vec/train_word2vec.py<br>
>[Wikipedia]https://ja.wikipedia.org/wiki/Wikipedia:%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89

