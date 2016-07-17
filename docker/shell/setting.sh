#!/bin/sh
if [ `stat -c "%U" /var/log/messages` = "root" ] ; then
  bash -lc 'find /var/log -type f | xargs -I{} rm {}'
fi

file=wtmp

dir=/var/log/

if [ -e $file ]; then
    echo "$file found."
else
    touch $dir$file 
    chown :utmp $dir$file 
fi

file=btmp

if [ -e $file ]; then
    echo "$file found."
else
    touch $dir$file 
    chown :utmp $dir$file 
fi


file=lastlog

if [ -e $file ]; then
    echo "$file found."
else
    touch $dir$file
    chown :syslog $dir$file
fi
