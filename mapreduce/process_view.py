import couchdb


server = "http://admin:admin@172.26.134.56:5984/"
couch = couchdb.Server(server)


view_results_australia_tweet = "view_results(australia_tweets)"
db_results_australia_tweet = couch[view_results_australia_tweet]


# sentiment count -> percent (australia_tweets)
def computePercent(senti, tt, id):
    keys = []
    for row in senti:
        keys.append(row['key'][0])

    items = {
        "_id": id,
        "rows": []
    }
    for row in senti:
        for r in tt:
            if row['key'][0] == r['key']:
                item = {}
                item['key'] = row['key']
                item['value'] = row['value']/r['value']
                items['rows'].append(item)
                break

    if id in db_results_australia_tweet:
        del db_results_australia_tweet[id]
    db_results_australia_tweet.save(items)

computePercent(db_results_australia_tweet["city_alcohol_senti_count"]['rows'],
               db_results_australia_tweet['city_alcohol_count']['rows'],
               "city_alcohol_senti_percent")
print("saved city_alcohol_senti_percent to db")

computePercent(db_results_australia_tweet["sa2_alcohol_senti_count"]['rows'],
               db_results_australia_tweet['sa2_alcohol_count']['rows'],
               "sa2_alcohol_senti_percent")
print("saved sa2_alcohol_senti_percent to db")

computePercent(db_results_australia_tweet["state_alcohol_senti_count"]['rows'],
               db_results_australia_tweet['state_alcohol_count']['rows'],
               "state_alcohol_senti_percent")
print("saved state_alcohol_senti_percent to db")


#####


# australia sentiment -> percent (australia_tweets)

aus_senti = db_results_australia_tweet['australia_alcohol_senti_count']['rows']
count = 0
for row in aus_senti:
    count += row['value']

id1 = "australia_alcohol_senti_percent"
items = {
    "_id": id1,
    "rows": []
}
for row in aus_senti:
    item1 = {}
    item1['key'] = row['key']
    item1['value'] = row['value'] / count
    items['rows'].append(item1)

if id1 in db_results_australia_tweet:
    del db_results_australia_tweet[id1]
db_results_australia_tweet.save(items)
print("saved australia_alcohol_senti_percent to db")



