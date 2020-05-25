
import json
import couchdb

file = open("../aurin/aurin_result/alcohol_sentiment.json", encoding='utf8').read()
data = json.loads(file)

file = open("../aurin/aurin_result/alcohol_sentiment.json", encoding='utf8').read()
data1 = json.loads(file)


server = "http://admin:admin@172.26.134.56:5984/"
couch = couchdb.Server(server)

database_name = "aurin_result"

try:
    db = couch[database_name]
except couchdb.http.ResourceNotFound:
    db = couch.create(database_name)

db_results_australia_tweet = couch["view_results(australia_tweets)"]

data_alcohol_senti_avg = db_results_australia_tweet['state_alcohol_senti_avg']['rows']
data_alltopic_senti_avg = db_results_australia_tweet['state_alltopic_senti_avg']['rows']

data['_id'] = "alcohol_sentiment"
data1['_id'] = "alltopic_sentiment"



def process(state1, state2):
    state_alcohol = data['data'][state1]
    state_alltopic = data1['data'][state1]
    for d in data_alcohol_senti_avg:
        if d['key'] == state2:
            state_alcohol['value'] = d['value']
            break
    for d in data_alltopic_senti_avg:
        if d['key'] == state2:
            state_alltopic['value'] = d['value']
            break


process("NAW","New South Wales")
process("QLD","Queensland")
process("SA", "South Australia")
process("TAS", "Tasmania")
process("VIC", "Victoria")
process("WA", "Western Australia")
process("ACT", "Australian Capital Territory")
process("NT",  "Northern Territory")

if "alcohol_sentiment" in db:
    del db['alcohol_sentiment']
db.save(data)
print("saved alcohol_sentiment to aurin_result")

if "alltopic_sentiment" in db:
    del db["alltopic_sentiment"]
db.save(data1)
print("saved alltopic_sentiment to aurin_result")

