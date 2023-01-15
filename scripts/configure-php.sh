#!/usr/bin/env zsh

VERSION=$(basename $(pwd) | sed -r 's/^(php-[0-9]\.[0-9]).*$/\1/')
PREFIX=~/.opt/$VERSION
PHP_INI_DIR=~/.config/$VERSION

./configure \
    --prefix=$PREFIX \
    --with-config-file-path=$PHP_INI_DIR \
    --with-config-file-scan-dir=$PHP_INI_DIR/conf.d \
    --enable-bcmath \
    --enable-calendar \
    --enable-exif \
    --enable-gd \
    --enable-intl \
    --enable-mbstring \
    --enable-mysqlnd \
    --enable-opcache \
    --enable-opcache-jit \
    --enable-sockets \
    --enable-zts \
    --with-curl \
    --with-freetype \
    --with-jpeg \
    --with-mhash \
    --with-mysqli \
    --with-openssl \
    --with-pdo-mysql \
    --with-pdo-pgsql \
    --with-pear \
    --with-pgsql \
    --with-readline \
    --with-sodium \
    --with-webp \
    --with-xpm \
    --with-xsl \
    --with-zip \
    --with-zlib

exit 0
