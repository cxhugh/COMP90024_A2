import json
import couchdb


server = "http://admin:admin@172.26.134.56:5984/"
couch = couchdb.Server(server)

db_results_australia_tweet = couch["view_results(australia_tweets)"]

try:
    db = couch["aurin_result"]
except couchdb.http.ResourceNotFound:
    db = couch.create("aurin_result")

file = open("../geojson_data/states.json", encoding = 'utf8').read()
geojson = json.loads(file)
geojson['_id'] = 'state_map_twitter_data'


data_alcohol_count = db_results_australia_tweet['state_alcohol_count']['rows']
data_alcohol_senti_avg = db_results_australia_tweet['state_alcohol_senti_avg']['rows']
data_alltopic_count = db_results_australia_tweet['state_alltopic_count']['rows']
data_alltopic_senti_avg = db_results_australia_tweet['state_alltopic_senti_avg']['rows']

file = open("../aurin/aurin_result/state_population.json", encoding = 'utf8').read()
data_state_population  = json.loads(file)


for item in geojson['features']:
    name = item['properties']['STATE_NAME']
    for d in data_alcohol_count:
        if d['key'] == name:
            item['properties']['alcohol_count'] = d['value']
            break
    for d in data_alcohol_senti_avg:
        if d['key'] == name:
            item['properties']['alcohol_sentiment_avg'] = d['value']
            break
    for d in data_state_population:
        if d["state"] == name:
            item['properties']['state_population'] = d['population']
            break
    for d in data_alltopic_count:
        if d['key'] == name:
            item['properties']['alltopic_count'] = d['value']
            break
    for d in data_alltopic_senti_avg:
        if d['key'] == name:
            item['properties']['alltopic_sentiment_avg'] = d['value']
            break



if 'state_map_twitter_data' in db:
    del db['state_map_twitter_data']
db.save(geojson)
print("saved state_map_twitter_data to db")


