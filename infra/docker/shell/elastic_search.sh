#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Elastic Search
#
#          library for Unix shell scripts.
#
#          Usage:
#              sh shell/elastic_search.sh [KEYWORD]
# ------------------------------------------------------------------

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
if [ $# -ne 1 ]; then
    echo "$0 [KEYWORD]"
    exit 1
fi

KEYWORD=$1

curl -XGET 'localhost:9200/_all/_search?pretty' -d'
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "title": {
              "query": "${KEYWORD}",
              "boost": 10
            }
          }
        },
        {
          "match": {
            "abstract": "${KEYWORD}"
          }
        }
      ]
    }
  }
}'
# -----------------------------------------------------------------
