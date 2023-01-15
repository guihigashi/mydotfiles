#!/usr/bin/env zsh

if [[ $1 == "" ]]; then
    echo provide version. 7.3, 8.0...
    exit 1
fi

ln -nsf $(realpath ~/.opt/php-$1) ~/.opt/php

exit 0
