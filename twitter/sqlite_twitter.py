#!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3

import sqlite3
import MeCab
import yaml
from collections import namedtuple

Twitter = namedtuple("Twitter", ["mecab"])
config_file = "enviroment.yml"

with open(config_file, encoding="utf-8") as cf:
    e = yaml.load(cf)
    twitter = Twitter(e["twitter"]["mecab"])

tagger = MeCab.Tagger("-Owakati -d %s" % twitter.mecab)
conn = sqlite3.connect('./twitter_data.db')
cur = conn.cursor()
cur.execute("""SELECT source_txt, replay_txt FROM ms_rinna;""")
source_file = open('source_twitter_data.txt', 'w')
replay_file = open('replay_twitter_data.txt', 'w')
for source_txt, replay_txt in cur.fetchall():
    replay_file.write(tagger.parse(source_txt).replace("\n", "") + '\n')
    source_file.write(tagger.parse(replay_txt).replace('\n', '') + '\n')

source_file.close()
replay_file.close()
