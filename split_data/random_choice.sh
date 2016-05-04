#!/bin/bash
# ------------------------------------------------------------------
# [Masaya Ogushi] Separate the Code for Try to Light Wiki Vector
#
#          library for Unix shell scripts.
#          Reference
#               http://stackoverflow.com/questions/2153882/how-can-i-shuffle-the-lines-of-a-text-file-on-the-unix-command-line-or-in-a-shel
#            Shell template
#               http://stackoverflow.com/questions/14008125/shell-script-common-template
#
# ------------------------------------------------------------------
# --- Option processing --------------------------------------------
if [ $# == 0 ] ; then
    echo $USAGE
    exit 1;
fi

WIKI_VECTOR=$1
GET_NUMBER=200000

# -- Body ---------------------------------------------------------

cat $WIKI_VECTOR | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' | head -n $GET_NUMBER