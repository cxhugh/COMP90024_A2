#!/usr/bin/env bash

#
while true
do
    python request.py
    python process_view.py
    python state_map_twitter_data.py
    python sa2_map.py
    echo "sleep 3600 ..."
    sleep 3600
done

