#!/usr/bin/env bash

nohup sh request.sh > request.out 2>&1 &
echo "sleep 1800"
sleep 1800