#!/usr/bin/env bash


while true
do
    python3 request.py
    python3 process_view.py
    python3 state_map_twitter_data.py
    python3 sa2_map.py
    python3 state_sentiment.py
    sleep 1800
done
