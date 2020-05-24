import json
import couchdb
from tqdm import tqdm
# from mpi4py import MPI
import sys
sys.path.append("../")
from harvester.get_ips import get_dbserver_ip


class Cold_dataloader():
    
    def __init__(self):
        self.server = db_server = 'http://admin:admin@' + get_dbserver_ip() + ':5984'
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
            for i, line in tqdm(enumerate(f)):
                # if i % processes == rank:
                try:
                    line = line[:-2]
                    line = json.loads(line)
                except json.decoder.JSONDecodeError:
                    print("Malformed JSON. Cannot read the line.")
                    continue
                except Exception as e:
                    print(e)

                if line['doc']['_id'] not in self.db:
                    line['doc'].pop('_rev')
                    try:
                        self.db.save(line['doc']) 
                    except Exception as e:
                        print(e)
                        pass
        f.close()
 

if __name__ == "__main__":
    # comm = MPI.COMM_WORLD
    # rank = comm.Get_rank()
    # size = comm.Get_size()
    loader = Cold_dataloader()
    loader.get_db()
    loader.save_cold_data_to_db()
