
import json
import couchdb

file = open("../aurin/aurin_result/gender.json", encoding='utf8').read()
data = json.loads(file)

server = "http://admin:admin@172.26.134.56:5984/"
couch = couchdb.Server(server)

database_name = "aurin_result"

try:
    db = couch[database_name]
except couchdb.http.ResourceNotFound:
    db = couch.create(database_name)

file = open("../aurin_result/state_population.json", encoding = 'utf8').read()
data_state_population  = json.loads(file)


items = {
    "_id": "gender",
    "data": data
}

relation = {
    "Queensland": "Greater Brisbane",
    "South Australia" : "Greater Adelaide",
    "Tasmania" : "Greater Hobart",
    "Victoria": "Greater Melbourne",
    "Western Australia": "Greater Perth",
    "New South Wales" : "Greater Sydney",
    "Australian Capital Territory": "Australian Capital Territory",
    "Northern Territory": "Greater Darwin"
}


for item in items['data']:
    city = item['city']
    for d in data_state_population:
        if relation[d['state']] == city:
            item['population'] = d['population']
            break

if "gender" in db:
    del db['gender']
db.save(items)
