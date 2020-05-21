#!/usr/bin/env bash

python request.py
python process_view.py
python state_map_twitter_data.py
python sa2_map.py
python state_sentiment.py