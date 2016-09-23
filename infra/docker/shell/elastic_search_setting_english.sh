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
USER_PASS=e_pass

# Elasticsearchの起動
expect -c "
spawn sudo /etc/init.d/elasticsearch start
expect \"\[sudo\] password for ${USER}: \"
send -- \"${USER_PASS}\n\"
expect eof
exit 0"

sleep 10s
# 文書登録用テンプレートの反映
curl -XPUT localhost:9200/_template/contents --data-binary \
     "@config/elastic_index_template_english.json"
expect -c "
spawn sudo /etc/init.d/elasticsearch restart
expect \"\[sudo\] password for ${USER}: \"
send -- \"${USER_PASS}\n\"
expect eof
exit 0"
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

