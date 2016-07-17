#!/bin/sh

Pyenv=pyenv

dir=/usr/local/

if [ -e $dir$Pyenv ]; then
    echo "$file found."
else
    git clone git://github.com/yyuu/pyenv.git /usr/local/pyenv
    mkdir /usr/local/pyenv/shims
    mkdir /usr/local/pyenv/versions
fi

VirtualEnv=pyenv/plugins/pyenv-virtualenv

if [ -e $dir$VirtualEnv ]; then
    echo "$file found."
else
    git clone git://github.com/yyuu/pyenv-virtualenv.git /usr/local/pyenv/plugins/pyenv-virtualenv
fi

