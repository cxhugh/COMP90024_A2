import couchdb
import json
from couchdb import Session

auth = Session()
auth.name = "admin"
auth.password = "admin"

server = "http//172.26.130.151:5984/"
server2 = "http://172.26.128.114:5984/" #
local = "http://127.0.0.1:5984/"

#couch = couchdb.Server(server,session=auth)
couch = couchdb.Server(local)

#database_name = "test_db"
database_name = "aurin_age_db2"

try:
    db = couch[database_name]
except couchdb.http.ResourceNotFound:
    db = couch.create(database_name)


def process_json(data):
    count=0
    for d in data:
        item = {
            '_id': d['id'],
            'properties':d['properties']
        }
        try:
            db.save(item)
            count+=1
        except couchdb.http.ResourceConflict:
            print('already existed')
    print("finished")
    print("Inserted:{} rows".format(count))
    return

if __name__ == "__main__":
    file = open("../aurin/2016VICAgeDist.json", encoding='utf8').read()
    data = json.loads(file)
    data = data['features']
    process_json(data)
