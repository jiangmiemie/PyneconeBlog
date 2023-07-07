#!/bin/sh
/usr/local/bin/python3.10 init.py

lsof -i:8000
lsof -i:3000

kill -9 $(lsof -i tcp:8000 -t)
kill -9 $(lsof -i tcp:3000 -t)

pc init
nohup pc run --env prod &