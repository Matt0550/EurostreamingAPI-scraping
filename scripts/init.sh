#!/bin/bash

# Get PORT and HOST from environment variables
PORT=5000
if [ ! -z "$PUID" ] && [ ! -z "$PGID" ]; then
    groupmod -g $PGID $APP_USER
    usermod -u $PUID -g $PGID $APP_USER

    chown -R $PUID:$PGID /home/api

    exec gosu $APP_USER cd /home/api && uvicorn api:app --port $PORT
else
    chown -R 0:0 /home/api
    
    exec cd /home/api && uvicorn api:app --port $PORT
fi