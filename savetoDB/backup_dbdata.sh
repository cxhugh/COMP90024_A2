curl -X GET http://admin:admin@172.26.134.56:5984/view_results\(australia_tweets\)/_all_docs\?include_docs\=true > /var/lib/couchdb/backup_data_json/view_results\(australia_tweets\).json
aurin_resultcurl -X GET http://admin:admin@172.26.134.56:5984/aurin_result/_all_docs\?include_docs\=true > /var/lib/couchdb/backup_data_json/aurin_result.json
sleep 30
# aurin_resultcurl -X GET http://admin:admin@172.26.134.56:5984/australia_tweets/_all_docs\?include_docs\=true > /var/lib/couchdb/backup_data_json/australia_tweets.json