import json
import couchdb
from tqdm import tqdm

class Cold_dataloader():
    
    def __init__(self):
        self.server = "http://admin:admin@172.26.134.56:5984/"
        # self.server = "http://lzy:woaideni@127.0.0.1:5984/"
        self.couch = couchdb.Server(self.server)
        self.database_name = "australia_tweets"
        self.db = None

    def get_db(self):
        try:
            self.db = self.couch[self.database_name]
        except couchdb.http.ResourceNotFound:
            self.db = self.couch.create(self.database_name)

    def save_cold_data_to_db(self):
        print('start')
        with open('/Users/lizhengyang/Downloads/db.json','r') as f:
            data = json.load(f)
        f.close()
        count = 0
        for i in tqdm(data['rows']):
            if i['doc']['_id'] not in self.db:
                tweet = i['doc']
                tweet.pop('_rev')
                if count == 0:
                    print(i['doc'])
                    print(tweet)
                    count +=1
                try:
                    self.db.save(tweet)     
                except Exception as e:
                    print(e)
                    pass


if __name__ == "__main__":
    loader = Cold_dataloader()
    loader.get_db()
    loader.save_cold_data_to_db()
