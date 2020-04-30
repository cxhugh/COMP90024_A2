import couchdb
import json

server = "http://admin:admin@172.26.129.233:5984/"
#local = "http://127.0.0.1:5984/"

couch = couchdb.Server(server)
database_name = "aurin_school_db"

try:
    db = couch[database_name]
except couchdb.http.ResourceNotFound:
    db = couch.create(database_name)


def process_json(data):
    count=0
    for d in data:
        item = {
            '_id': d['id'],
            'geometry': d['geometry'],
            'properties': d['properties']
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
    file = open("../aurin/2016AustraliaSchoolProfile.json", encoding='utf8').read()
    data = json.loads(file)
    data = data['features']
    process_json(data)
