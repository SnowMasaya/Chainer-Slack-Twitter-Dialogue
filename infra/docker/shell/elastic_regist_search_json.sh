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

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
# Regist json bulk
for json_gz in $(ls data/*.json.gz)
do
    curl --compressed -H "Content-encoding: gzip" -XPOST http://localhost:9200/_bulk --data-binary \
                "@${json_gz}" > /dev/null
done
sleep 10s
# Check the regist data
curl 'localhost:9200/_cat/indices?v'
# -----------------------------------------------------------------
