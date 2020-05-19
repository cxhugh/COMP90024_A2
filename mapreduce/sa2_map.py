import json
import couchdb

file = open("../aurin/aurin_result/greaterMelbourne_sa2_map_aurin.json", encoding='utf8').read()
data = json.loads(file)
#print(data[0])


file = open("../geojson_data/SA2_2016_AUST_GreaterMelb.json", encoding = 'utf8').read()
geojson = json.loads(file)
geojson['_id'] = 'sa2_map_twitter'

server = "http://admin:admin@172.26.129.233:5984/"
couch = couchdb.Server(server)


try:
    db = couch["aurin_result"]
except couchdb.http.ResourceNotFound:
    db = couch.create("aurin_result")

db_results_australia_tweet = couch["view_results(australia_tweets)"]

data_alcohol_count = db_results_australia_tweet['sa2_alcohol_count']['rows']
data_alcohol_senti_avg = db_results_australia_tweet['sa2_alcohol_senti_avg']['rows']
data_alltopic_count = db_results_australia_tweet['sa2_alltopic_count']['rows']


for item in geojson['features']:
    name = item['properties']['SA2_NAME16']
    suburb_id = item['properties']['SA2_MAIN16']

    for d in data:
        if d['SA2_NAME16'] == name:
            item['properties']['unemployed_percent'] = d['unemployed_percent']
            item['properties']['population_density'] = d['population_density']
            item['properties']['equivalised_household_income_median'] = d['equivalised_household_income_median']
            item['properties']['degree_diploma_certificate_percent'] = d['degree_diploma_certificate_percent']
            #print(item['properties'])
            break

    for d in data_alcohol_count:
        if d['key'] == suburb_id:
            item['properties']['alcohol_count'] = d['value']
            break
    for d in data_alcohol_senti_avg:
        if d['key'] == suburb_id:
            item['properties']['alcohol_sentiment_avg'] = d['value']
            break
    for d in data_alltopic_count:
        if d["key"] == suburb_id:
            item['properties']['alltopic_count'] = d['value']
            break

if 'sa2_map_twitter' in db:
    del db['sa2_map_twitter']
db.save(geojson)
print("saved sa2_map_twitter to db")


