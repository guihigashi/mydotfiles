#!/usr/bin/env bash

set -x

url=https://api.github.com/repos/cosmtrek/air/releases/latest

LDFLAGS+="-X main.airVersion=$(curl $url -s | jq .name -r)"
LDFLAGS+=" -X main.goVersion=$(go version | sed -r 's/go version go(.*)\ .*/\1/')"

go install -ldflags "$LDFLAGS" github.com/cosmtrek/air@latest

exit 0
