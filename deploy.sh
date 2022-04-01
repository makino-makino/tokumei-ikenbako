#!/usr/bin/env bash

set -eux

LOG_ROOT=$HOME/log

## Save logs
(
    log_outpath="$LOG_ROOT/$(date +%y-%m-%d_%H-%M)"
    mkdir -p $log_outpath

    declare -a containers=(neo-polling_api_1 neo-polling_app_1 neo-polling_proxy_1)

    for container in "${containers[@]}"
    do
        logfile="$(docker inspect --format='{{.LogPath}}' $container)"
        log_outfile="$log_outpath/$container-json.log"
        sudo cp $logfile $log_outfile
        sudo chown $USER:$USER $log_outfile
    done
)

## Update
git pull

## Build crypto
(
    cd crypto
    sudo docker-compose build
    docker-compose up
)

## Restart service
docker-compose down
sudo docker-compose build
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
