import requests
import couchdb
import json
from create_view import *
from config import server_address


server = server_address()
couch = couchdb.Server(server)


view_results_australia_tweet = "view_results(australia_tweets)"
australia_tweet = "australia_tweets"

db_australia_tweet = couch[australia_tweet]

try:
    db_results_australia_tweet = couch[view_results_australia_tweet]
except couchdb.http.ResourceNotFound:
    db_results_australia_tweet = couch.create(view_results_australia_tweet)


def request(server, db_name, design_name, view_name, group_level):
    url = server + db_name + "/_design/" + design_name  +"/_view/" + view_name + "?group_level=" + str(group_level)

    response = requests.get(url)
    content = None
    if response.status_code == 200:
        content = response.json()
    elif response.status_code == 404:
        print("%s does not exist." % (view_name))
        return "404"
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


def request_and_save(server,viewdb_name,design_name, view_name, group_level,view_db,map_func, reduce_func,save_db,id):
    while True:
        print("requesting ...")
        response = request(server,viewdb_name,design_name,view_name,group_level)
        if response == "404":
            create_view(view_db,design_name,view_name,map_func,reduce_func)
            print("created view.")
        elif response != None:
            save_toDB(save_db,id,response)
            print("saved %s to db."%(id))
            #save_toJSON("%s.json"%(id),response)
            break

def request_and_save_top(server,viewdb_name,design_name, view_name, group_level,view_db,map_func, reduce_func,save_db,id):
    while True:
        print("requesting ...")
        response = request(server,viewdb_name,design_name,view_name,group_level)
        if response == "404":
            create_view(view_db,design_name,view_name,map_func,reduce_func)
            print("created view.")
        elif response != None:
            # sorting (sort by value)
            rows = response['rows']
            rows.sort(key=lambda x: x['value'], reverse=True)
            ans = rows[:20]
            #print(ans)
            item = {
                "_id": id,
                "rows": ans
            }
            if id in save_db:
                del save_db[id]
            save_db.save(item)
            print("saved %s to db."%(id))
            #save_toJSON("%s.json"%(id),item)
            break


if __name__ == "__main__":

    # australia tweet
    # state, all topic, count

    request_and_save(server, australia_tweet, "state", "alltopic_count", 1, db_australia_tweet,
                     map_function_alltopic_state_count,
                     reduce_function_count, db_results_australia_tweet, "state_alltopic_count")

    # state, alcohol, count
    request_and_save(server, australia_tweet, "state", "alcohol_count", 1, db_australia_tweet,
                     map_function_alcohol_state_count,
                     reduce_function_count, db_results_australia_tweet, "state_alcohol_count")

    # city, all topic, count
    request_and_save(server, australia_tweet, "city", "alltopic_count", 1, db_australia_tweet,
                     map_function_alltopic_city_count,
                     reduce_function_count, db_results_australia_tweet, "city_alltopic_count")

    # city, alcohol, count
    request_and_save(server, australia_tweet, "city", "alcohol_count", 1, db_australia_tweet,
                     map_function_alcohol_city_count,
                     reduce_function_count, db_results_australia_tweet, "city_alcohol_count")
    

    # sa2, all topic, count

    request_and_save(server, australia_tweet, "sa2", "alltopic_count",1, db_australia_tweet,
                     map_function_alltopic_sa2_count,
                     reduce_function_count, db_results_australia_tweet, "sa2_alltopic_count")

    # sa2, alcohol, count
    request_and_save(server, australia_tweet, "sa2", "alcohol_count",1, db_australia_tweet,
                     map_function_alcohol_sa2_count,
                     reduce_function_count, db_results_australia_tweet, "sa2_alcohol_count")
    
    # state, all topic, sentiment avg
    request_and_save(server, australia_tweet, "state", "alltopic_senti_avg",1, db_australia_tweet,
                     map_function_alltopic_state_senti_avg,
                     reduce_function_avg, db_results_australia_tweet, "state_alltopic_senti_avg")

    # state, alcohol, sentiment avg
    request_and_save(server, australia_tweet, "state", "alcohol_senti_avg", 1, db_australia_tweet,
                     map_function_alcohol_state_senti_avg,
                     reduce_function_avg, db_results_australia_tweet, "state_alcohol_senti_avg")

    # city, all topic, sentiment avg
    request_and_save(server, australia_tweet, "city", "alltopic_senti_avg",1 , db_australia_tweet,
                     map_function_alltopic_city_senti_avg,
                     reduce_function_avg, db_results_australia_tweet, "city_alltopic_senti_avg")

    # city, alcohol, sentiment avg
    request_and_save(server, australia_tweet, "city", "alcohol_senti_avg", 1, db_australia_tweet,
                     map_function_alcohol_city_senti_avg,
                     reduce_function_avg, db_results_australia_tweet, "city_alcohol_senti_avg")

    # sa2, all topic, sentiment avg
    request_and_save(server, australia_tweet, "sa2", "alltopic_senti_avg",1 , db_australia_tweet,
                     map_function_alltopic_sa2_senti_avg,
                     reduce_function_avg, db_results_australia_tweet, "sa2_alltopic_senti_avg")

    # sa2, alcohol, sentiment avg
    request_and_save(server, australia_tweet, "sa2", "alcohol_senti_avg",1, db_australia_tweet,
                     map_function_alcohol_sa2_senti_avg,
                     reduce_function_avg, db_results_australia_tweet, "sa2_alcohol_senti_avg")


    # state, alcohol, sentiment count
    request_and_save(server, australia_tweet, "state", "alcohol_senti_count", 2, db_australia_tweet,
                     map_function_alcohol_state_senti_count,
                     reduce_function_count, db_results_australia_tweet, "state_alcohol_senti_count")


    # city, alcohol, sentiment count
    request_and_save(server, australia_tweet, "city", "alcohol_senti_count",2, db_australia_tweet,
                     map_function_alcohol_city_senti_count,
                     reduce_function_count, db_results_australia_tweet, "city_alcohol_senti_count")


    # sa2, alcohol, sentiment count
    request_and_save(server, australia_tweet, "sa2", "alcohol_senti_count",2, db_australia_tweet,
                     map_function_alcohol_sa2_senti_count,
                     reduce_function_count, db_results_australia_tweet, "sa2_alcohol_senti_count")

    # australia, alcohol,sentiment count
    request_and_save(server, australia_tweet, "australia2", "alcohol_senti_count",1, db_australia_tweet,
                     map_function_alcohol_australia_senti_count,
                     reduce_function_count, db_results_australia_tweet, "australia_alcohol_senti_count")


    request_and_save_top(server, australia_tweet, "australia2", "alltopic_hashtag_count", 1, db_australia_tweet,
                         map_function_alltopic_australia_hashtag_count,
                         reduce_function_count, db_results_australia_tweet, "australia_hashtag_count")


    request_and_save_top(server, australia_tweet, "australia2", "alcohol_hashtag_count", 1, db_australia_tweet,
                     map_function_alcohol_australia_hashtag_count,
                     reduce_function_count, db_results_australia_tweet, "australia_alcohol_hashtag_count")




