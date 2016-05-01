Chainer-Slack-Twitter-Dialogue
====

This tool is making Dialogue Model for Slack

Thsi tool has 3 functions

1: Slack Communication
2: Learning by the Chainer 
3: Collect Twitter Data

## Description
This tool is making the Dialogue Model

If you see the detail about it, you see the below<br> 

http://qiita.com/GushiSnow/items/79ca7deeb976f50126d7

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
pip install chainer=="1.5.1"
```

####Prepare the Data

```
PreTrain
>[Wikipedia for Japanese]https://dumps.wikimedia.org/jawiki/latest/<br>
Train
>[Dialogue Data]https://sites.google.com/site/dialoguebreakdowndetection/<br>
```
SQLite

```
touch twitter_data.db
```

### How to prepare the for dialogue Data

#### About Wikipedia Data

1: You set the wikipedia title data on the word2vec folder

2: Rename the data to `jawiki-latest-all-titles-in-ns0`

3: You execute the bellow script. You can get the Word2Vec Model

https://github.com/SnowMasaya/Chainer-Slack-Twitter-Dialogue/blob/master/word2vec/word2vec_execute.py

*

If you try to confirm the this code, you have to reduce the wikipedia data.
The below script is the get the 5000 random data

```
sh random_choice.sh {Wikipedia Title data name} > {Random 5000 Choosing Wikipedia Title data name}
```

https://github.com/SnowMasaya/Chainer-Slack-Twitter-Dialogue/blob/master/word2vec/random_choice.sh

#### About Dialogue Data

1: You have to make the `data` folder

2: You get the [Broken Dialogue corpus](https://sites.google.com/site/dialoguebreakdowndetection/). And you make the file bellow

```
dev/〇〇.json
dev/■ ■.json
dev/◇◇◇.json
```

3: It is possible to split the data `player_1`, `player_2` in the bellow script

https://github.com/SnowMasaya/Chainer-Slack-Twitter-Dialogue/blob/master/data_load.py

4: You have to split the each word in the sentence. You use [mecab](http://mecab.googlecode.com/svn/trunk/mecab/doc/index.html?sess=3f6a4f9896295ef2480fa2482de521f6) library.
And you set the bellow data on the `data` folder 

```
player_1_wakati
player_2_wakati
```

####Prepare Twitter Key

```
https://apps.twitter.com/
```

####Prepare enviroment.yml

Twitter

```
twitter:
    consumer_key: your consumer key 
    consumer_secret: your consumer secret
    token: your api token
    token_secret: your token secret
    mecab: your mecab dictionary
```


Slack

```
slack:
    api_token: your api token 
    channel: your channel 
    user: your user token
    mecab: your mecab dictionary 
```


Installing a library bellow

##Requirements


```
    Python 3.4+
	Mecab and neolog-dict
	numpy
    chainer
    ipython
    notebook
    jinja2
    pyzmq
    tornado
    cython
    gensim
    PyYAML
    requests
    requests_oauthlib
    djehuty
    flask-slackbot
    flask
    mecab-python
    future
    websocket-client
```

####Confirm library

```
ipython
```

#
### Usage 
#
Learning Chainer

```
*You execute python 
ipython notebook
```

Slack Communication

```
*You execute python
cd slack
python app.py
```

Get the Twitter Data

```
*You execute python
cd twitter
python twitter_get_usr_timeline.py
python sqlite_twitter.py
```

#
### Code Directory Structure 
#
```
Dialogue ipython notebook and Encoder Decoder Model
  - slack/　　　　　... Slack Code
  - util/　     　... Encoder Decoder tools
  - twitter/ 　　　　　　　... Twitter Code
  - word2vec/ 　　　　　　　... Word2Vec Code
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

