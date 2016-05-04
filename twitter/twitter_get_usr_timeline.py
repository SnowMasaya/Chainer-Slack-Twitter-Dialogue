#!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/python3

from requests_oauthlib import OAuth1Session
import yaml
from collections import namedtuple
import json
import sqlite3
import re


class TwitterGetUserTimeline():
    """
    This module for the getting the twitter dialogue text
    """

    def __init__(self):
        """
        Setting initial paramater
        :return:
        """
        Twitter = namedtuple("Twitter", ["consumer_key", "consumer_secret", "token", "token_secret"])
        config_file = "enviroment.yml"

        with open(config_file, encoding="utf-8") as cf:
             e = yaml.load(cf)
             twitter = Twitter(e["twitter"]["consumer_key"], e["twitter"]["consumer_secret"],
                               e["twitter"]["token"], e["twitter"]["token_secret"])

        CK = twitter.consumer_key         # Consumer Key
        CS = twitter.consumer_secret      # Consumer Secret
        AT = twitter.token                # Access Token
        AS = twitter.token_secret         # Accesss Token Secert

        # ツイート投稿用のURL
        self.url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

        # ツイート本文
        self.screen_name = "ms_rinna"
        self.params = {"screen_name": self.screen_name, "exclude_replies": False, "count": 1000}

        # OAuth認証で POST method で投稿
        self.twitter = OAuth1Session(CK, CS, AT, AS)
        self.twitter_txt_dict = {}
        self.p = re.compile(r"@.* ")
        self.conn = sqlite3.connect('./twitter_data.db')
        self.cur = self.conn.cursor()
        self.first_sqlite()

    def first_sqlite(self):
        """
        Make the table for SQLite
        """
        self.cur.execute(""" SELECT COUNT(*) FROM sqlite_master WHERE name = ?  """, (self.screen_name, ))
        res = self.cur.fetchone()
        if bool(res[0]) == False:
            print("""CREATE TABLE %s(id serial, source_txt text, replay_txt text);""" % self.screen_name)
            self.cur.execute("""CREATE TABLE %s(id serial, source_txt text, replay_txt text);""" % self.screen_name)


    def twitter_method(self, req, dict_flag=True, dict_value={}):
        if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
            timeline = json.loads(req.text)
            # 各ツイートの本文を表示
            if(dict_flag):
                for tweet in timeline:
                    self.meke_dict(tweet)
            else:
                for tweet in timeline:
                    self.check_dict(tweet, v)
        else:
            # エラーの場合
            print ("Error: %d" % req.status_code)

    def meke_dict(self, tweet):
        """
        make for the twitter dialogue dict
        :param tweet: tweet_data
        :return:
        """
        if tweet["in_reply_to_screen_name"] not in self.twitter_txt_dict:
            self.twitter_txt_dict[tweet["in_reply_to_screen_name"]] = {}
            self.twitter_txt_dict[tweet["in_reply_to_screen_name"]][tweet["in_reply_to_status_id"]] = tweet["text"]
        else:
            self.twitter_txt_dict[tweet["in_reply_to_screen_name"]][tweet["in_reply_to_status_id"]] = tweet["text"]

    def insert_sqlite(self, id, s_txt, r_txt):
        """
        Insert source text and reply text
        :param id:
        :param s_txt:
        :param r_txt:
        :return:
        """
        print("""INSERT INTO %s(source_txt, replay_txt) VALUES(\"%s\", \"%s\")""" % (self.screen_name, s_txt, r_txt))
        values = (id, s_txt, r_txt)
        self.cur.execute("""INSERT INTO %s(id, source_txt, replay_txt) VALUES (?, ?, ?)""" % self.screen_name, values)

    def check_dict(self, tweet, source_dict):
        """
        :param tweet:
        :param source_dict: twitter account tweet contents
        :return:
        """
        for k, v in source_dict.items():
            if tweet["id"] == k:
                source_txt = self.p.sub("", v)
                replay_txt = self.p.sub("", tweet["text"])
                self.insert_sqlite(k, source_txt, replay_txt)

if __name__ == '__main__':
    twitter_get_user_timeline = TwitterGetUserTimeline()
    req = twitter_get_user_timeline.twitter.get(twitter_get_user_timeline.url, params = twitter_get_user_timeline.params)
    # Twitter
    twitter_get_user_timeline.twitter_method(req)
    for k,v in twitter_get_user_timeline.twitter_txt_dict.items():
        params = {"screen_name": k, "exclude_replies": False, "count": 1000}
        req = twitter_get_user_timeline.twitter.get(twitter_get_user_timeline.url, params = params)
        twitter_get_user_timeline.twitter_method(req, dict_flag=False, dict_value=v)
    # SQLite
    twitter_get_user_timeline.conn.commit()
    twitter_get_user_timeline.conn.close()
