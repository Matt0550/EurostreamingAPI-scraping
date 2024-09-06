#!/bin/bash

# Get PORT and HOST from environment variables
PORT=5000
HOST="0.0.0.0"

if [ ! -z "$PUID" ] && [ ! -z "$PGID" ]; then
    groupmod -g $PGID $APP_USER
    usermod -u $PUID -g $PGID $APP_USER

    chown -R $PUID:$PGID /home/api
    # Workdir
    cd /home/api

    exec gosu $APP_USER uvicorn api:app --port $PORT --host $HOST
else
    chown -R 0:0 /home/api
    
    # Workdir
    cd /home/api

    exec uvicorn api:app --port $PORT --host $HOST
fi