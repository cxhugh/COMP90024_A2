import requests
import json
import couchdb
from couchdb import Session


auth = Session()
auth.name = "admin"
auth.password = "admin"

#server = "http//172.26.130.151:5984/"
local = "http://127.0.0.1:5984/"

#couch = couchdb.Server(server,session=auth)
couch = couchdb.Server(local)

#database_name = "test_db"
database_name = "aurin_school_db2"
db = couch[database_name]


def request(server, db_name, design_name, view_name):
    url = server + db_name + "/_design/" + design_name + "/_view/" + view_name + "?group_level=1"
    response = requests.get(url)
    content = None
    if response.status_code == 200:
        content = response.json()
    return content


def save_toDB(db,id,response):
    if id in db:
        del db[id]
    result = {
        "_id": id,
        "rows": response['rows'],
    }
    db.save(result)


def save_toJSON(file_name, response):
    with open(file_name, 'w') as f:
        json.dump(response, f, indent=4)


if __name__ == "__main__":
    schoolCount_response = request(local, database_name, "state", "schoolCount")
    ttEnrolment_response = request(local, database_name, "state", "ttEnrolment")
    schoolSector_response = request(local, database_name, "state", "schoolSector")

    save_toDB(db,"state_school_count",schoolCount_response)
    save_toDB(db, "state_ttEnrolment_count", ttEnrolment_response)
    save_toDB(db, "state_schoolSector", schoolSector_response)

    save_toJSON("viewResults/state_school_count.json", schoolCount_response)

