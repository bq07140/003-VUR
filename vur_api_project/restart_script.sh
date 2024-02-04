#!/bin/bash
lsof -i :5000 | awk 'NR!=1 {print $2}' | xargs kill -9
nohup python3 ./vur_api_run.py &
