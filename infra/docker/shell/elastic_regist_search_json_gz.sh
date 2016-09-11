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
if [ $# -ne 1 ]; then
    echo "$0 [data name] "
    exit 1
fi
JSON_GZ=$1

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
# Regist json bulk
curl --compressed -H "Content-encoding: gzip" -XPOST http://localhost:9200/_bulk --data-binary \
                "@${JSON_GZ}" > /dev/null
# -----------------------------------------------------------------
