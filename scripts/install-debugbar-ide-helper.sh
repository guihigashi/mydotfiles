#!/usr/bin/env bash

for i in debugbar ide-helper; do
    if ! [ -n "$(composer show -N | grep barryvdh/laravel-$i)" ]; then
        composer require --dev "barryvdh/laravel-$i"
    fi
done

php artisan ide-helper:generate
php artisan ide-helper:meta
php artisan ide-helper:models --write-mixin
