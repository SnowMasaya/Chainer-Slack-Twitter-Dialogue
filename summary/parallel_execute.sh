#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Parallerl Script for multi thread
#                 Execute using the parallel script for multi thread producer and consumer partern
#
#          library for Unix shell scripts.
#          Reference
#               https://www.gnu.org/software/parallel/man.html
#            Japanese
#               http://bicycle1885.hatenablog.com/entry/2014/08/10/143612
#            Shell template
#               http://stackoverflow.com/questions/14008125/shell-script-common-template
#
# ------------------------------------------------------------------

# -- Body ---------------------------------------------------------
#  SCRIPT LOGIC GOES HERE
ROOT_DIR=`pwd`

# Execute Parallel command
# If you check the which program run, you run the bellow command
# `--dry-run` option is show the command
cat $ROOT_DIR/../Data/wn_summary_list_split.txt | parallel -a - --dry-run python $ROOT_DIR/test/multi_thread_producer_consumer_class_summary.py -r
cat $ROOT_DIR/../Data/wn_summary_list_split.txt | parallel -j 2 -a - python $ROOT_DIR/test/multi_thread_producer_consumer_class_summary.py -r & 
