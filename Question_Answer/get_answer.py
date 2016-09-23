#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from os import path
APP_ROOT = path.dirname( path.abspath( __file__ ) )
from elasticsearch import Elasticsearch
from elasticsearch import helpers


class GetAnswer():
    """
    Get the Answer by the Elasticsearch
    Reference
        http://elasticsearch-py.readthedocs.io/en/master/api.html
    """

    def __init__(self):
        """
        Setting initial data
        """
        self.es = Elasticsearch(['elasticsearch_dialogue', 'elasticsearch_dialogue_english'], port=9200,)
        self.doc = {}
        self.elastic_index = "_all"
        self.search_result = []

    def search_data(self, search_key_word):
        """
        search data into the elastic search
        param: search_keyword: you set the search key word
        """
        self.search_result = []
        self.setting_search_query(search_key_word)
        self.res = self.es.search(index=self.elastic_index, body=self.query)
        for hit in self.res['hits']['hits']:
            self.search_result.append(hit["_source"])

    def setting_search_query(self, search_key_word):
        """
        transform the seach key word into the query
        param: search_keyword: you set the search key word
        """
        self.query = {
            "query": {
              "bool": {
                "should": [
                  {
                    "match": {
                      "title": {
                        "query": "\"" + search_key_word + "\"",
                        "boost": 10
                      }
                    }
                  },
                  {
                    "match": {
                      "abstract": "\"" + search_key_word + "\""
                    }
                  }
                ]
              }
            }
        }

