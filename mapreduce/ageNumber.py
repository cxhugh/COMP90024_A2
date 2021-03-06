
import json
import couchdb
from config import server_address

file = open("../aurin/aurin_result/ageGroup_number.json", encoding='utf8').read()
data = json.loads(file)


server = server_address()
couch = couchdb.Server(server)

database_name = "aurin_result"

try:
    db = couch[database_name]
except couchdb.http.ResourceNotFound:
    db = couch.create(database_name)


items = {
    "_id": "age_number",
    "data": data
}

if "age_number" in db:
    del db['age_number']
db.save(items)
