#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Elastic Search Regist shell
#
#    library for Unix shell scripts.
#    Usage
#           you have to use this script `sudo` command in the docker enviroment
#    Reference
#        http://dev.classmethod.jp/tool/jq-manual-japanese-translation-roughly/
#
# ------------------------------------------------------------------
if [ $# -ne 2 ]; then
    echo "$0 [PIPE_NUMBER] [PARALLEL_NUMBER]"
    exit 1
fi

PIPE_NUMBER=$1
PARALLEL_NUMBER=$2
PARALLEL=/usr/local/bin/parallel
# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
# Regist json bulk
ls data/*.json.gz > data/json_gz_list
cat data/json_gz_list | $PARALLEL --linebuffer --pipe -N $PIPE_NUMBER --round-robin -j${PIPE_NUMBER} $PARALLEL --linebuffer -j $PARALLEL_NUMBER -a - sh shell/elastic_regist_search_json_gz.sh ::: 1
sleep 10s
# Check the regist data
curl 'localhost:9200/_cat/indices?v'
# -----------------------------------------------------------------
