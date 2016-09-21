#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname("__file__"), "."))
from os import path
APP_ROOT = path.dirname(path.abspath("__file__"))
import mysql.connector
import yaml
from mysql.connector import errorcode


class WikiPediaImageLink():
    """
    Wikipedia get the image link
    MySQL for Python Reference
        https://dev.mysql.com/doc/connector-python/en
    you have to install the mysql
        http://dev.mysql.com/doc/refman/5.7/en/installing.html
    GEt the source code latest versions
         http://dev.mysql.com/downloads/connector/python/
    Install the mysql for python
         cd {your} download directory
         tar xzf mysql-connector-python-VER.tar.gz
         cd mysql-connector-python-VER
         sudo python setup.py install
    you have to set the data in the mysql
    Data:
        https://archive.org/download/enwiki-20080312
    """

    def __init__(self):
        self.config_file = APP_ROOT + "/conf/mysql_info.yml"
        self.__read_config()
        self.image_data_list = []
        self.format = "https://en.wikipedia.org/wiki/File:"
        self.start_mysql()

    def __read_config(self):
        """
        read config file for mysql
        """
        with open(self.config_file, encoding="utf-8") as cf:
           e = yaml.load(cf)
           self.user = e["mysql"]["user"]
           self.password = e["mysql"]["password"]
           self.host = e["mysql"]["host"]
           self.database = e["mysql"]["database"]

    def start_mysql(self):
        """
        Start the MySQL
        :return:
        """
        try:
            self.cnx = mysql.connector.connect(user=self.user, password=self.password,
                                          host=self.host,
                                          database=self.database)
            self.cursor = self.cnx.cursor(buffered=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def search_like(self, search_word):
        """
        MySQL like search
        :param search_word(string):
        :return:
        """
        query = "SELECT DISTINCT il_to from imagelinks WHERE (il_to LIKE " + "'" + search_word  + "%" + ".jpg')" + "OR" + \
                "(il_to LIKE " + "'" + search_word  + "%" + ".JPG')" +  "order by (il_to = '" + search_word + "') desc"
        try:
            self.cursor.execute(query)
        except:
            print(mysql.connector.Error)
        # Get the byte array data, convert the bytearray to string
        #     http://stackoverflow.com/questions/10459067/how-to-convert-my-bytearrayb-x9e-x18k-x9a-to-something-like-this-x9e-x1
        for il_to in self.cursor:
            self.image_data_list.append(self.format + il_to[0].decode("utf-8"))

    def end_use_mysql(self):
        """
        Call Dont use mysql
        """
        self.image_data_list = []
        self.cnx.close()

