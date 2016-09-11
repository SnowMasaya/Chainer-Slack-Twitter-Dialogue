#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Elastic Search
#
#          library for Unix shell scripts.
#
#          Usage:
#              sh shell/elastic_search.sh [KEYWORD]
#          If you use the container, you use the --link option
#               docker run --link {elasticsearch running continaer id} -it docker_dialogue/dialogue bash
#          Confirm the other ip address
#               docker inspect {your container id} | grep IPAddress
# ------------------------------------------------------------------

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
if [ $# -ne 1 ]; then
    echo "$0 [KEYWORD]"
    exit 1
fi

DOUBLE_QUOTE="\""
KEYWORD=${DOUBLE_QUOTE}${1}${DOUBLE_QUOTE}

curl -XGET 'elasticsearch_dialogue:9200/_all/_search?pretty' -d'
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "title": {
              "query": '$KEYWORD',
              "boost": 10
            }
          }
        },
        {
          "match": {
            "abstract": '$KEYWORD'
          }
        }
      ]
    }
  }
}'
# -----------------------------------------------------------------