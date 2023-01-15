#!/usr/bin/zsh

set -x

url=https://api.github.com/repos/FiloSottile/mkcert/releases/latest

LDFLAGS+="-X main.Version=$(curl $url -s | jq .tag_name -r)"

go install -ldflags "$LDFLAGS" filippo.io/mkcert@latest

exit 0
