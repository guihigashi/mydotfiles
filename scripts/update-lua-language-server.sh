#!/usr/bin/env zsh

dest="$HOME/.opt/lua-language-server"

download_url=$(
    curl -sL https://api.github.com/repos/sumneko/lua-language-server/releases/latest |
        jq -r '.assets[] | select(.name | test("linux-x64.tar.gz$")) | .browser_download_url'
)
archive=$(mktemp)
curl -Lo $archive $download_url

mkdir -p $dest
rm -rf $dest/*
tar -xf $archive -C $dest

exit 0
