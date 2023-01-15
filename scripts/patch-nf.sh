#!/usr/bin/env zsh

if [[ $1 == "" || $2 == "" ]]; then
    echo provide source and destination
    exit 1
fi

mkdir -p $2

src=$(realpath $1)
dst=$(realpath $2)

docker run --rm -v $src:/in -v $dst:/out nerdfonts/patcher -s -l -c
