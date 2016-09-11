#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Elastic First Setting
#
#          library for Unix shell scripts.
#
# ------------------------------------------------------------------

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
ROOT_DIR=`pwd`

# Elasticsearchの起動
sudo /etc/init.d/elasticsearch start &
sleep 10s
# 文書登録用テンプレートの反映
curl -XPUT localhost:9200/_template/contents --data-binary \
     "@config/elastic_index_template.json"
sudo /etc/init.d/elasticsearch restart
sleep 10s
echo Register
# 文書登録処理
curl -X POST http://localhost:9200/contents-2016/contents/1  -d '
{
    "body_text" : "今回、作成したUbuntuでのDocker環境の構築方法です。"
}
'
sleep 1s
echo Search
# 文書検索処理
curl -XGET 'localhost:9200/contents-2016/contents/_search?pretty' -d'
{
 "query":{"match":{"body_text":"Ubuntu"}}
}'
# 登録された文書の確認
curl 'localhost:9200/_cat/indices?v'
# -----------------------------------------------------------------

