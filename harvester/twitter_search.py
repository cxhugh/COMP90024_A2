import tweepy
import sys, getopt
import couchdb
# import mpi4py
import json
import os

# CONSTANT
TWEETSPREQUERY = 100 # max
geocode_mel = "-37.813629,144.963058,60km"
# db_server = 'http://lzy:woaideni@127.0.0.1:5984'

db_server = 'http://admin:admin@172.26.129.233:5984'


def generate_api(key_group):
    with open('api_keys.json','r') as f:
        keys = f.read()
        keys = json.loads(keys)
    f.close()    
    
    if key_group == "api-1":
        consumer_key = keys['api-1']['consumer_key']
        consumer_secret = keys['api-1']['consumer_secret']
        access_token = keys['api-1']['access_token']
        access_token_secret = keys['api-1']['access_token_secret']

    print("start Oauth API")
    # Creating the authentication object
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    # Setting access token and secret
    auth.set_access_token(access_token,access_token_secret)
    # Creating the API object while passing in auth information
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    if (not api):
        print("Can't Authenticate")
        sys.exit(-1)

    return api

def search_tweets(query,api,db):
    sinceId = None
    max_id = -1
    request_times = 0
    finish_state = False
    while True:
        try:
            if max_id <= 0:
                # search api returns from big id to small id
                tweets_list = api.search(q=query,geocode=geocode_mel,count=TWEETSPREQUERY,
                    tweet_mode="extended")
            else:
                # search start from previous biggest one - 1, avoid redundency
                tweets_list = api.search(q=query,geocode=geocode_mel,count=TWEETSPREQUERY,
                    tweet_mode="extended",max_id=str(max_id-1))
            request_times += 1
            print('send request ',request_times)

            if not tweets_list:
                print("no new twitter found")
                finish_state = True
                break
            
            max_id = tweets_list[-1].id
            for t in tweets_list:               
                tweet = t._json
                # print(tweet._json['text'])
                # with_location = False
                # if tweet['geo'] or tweet['coordinates'] or tweet['place']:
                #     with_location = True
                # if 'location' in tweet:
                #     print(tweet['location'])

                filter_tweet_info = {'_id':tweet['id_str'],
                    'created_at':tweet['created_at'],
                    'text':tweet['full_text'],
                    'user':tweet['user'],
                    'place_info':{'geo':tweet['geo'],'coordinates':tweet['coordinates'],'place':tweet['place']},
                    'city':'Melbourne',
                    'geocode':(-37.813629,144.963058)}

                if filter_tweet_info['_id'] not in db:
                    db.save(filter_tweet_info)

                # if tweet['geo'] and 'coordinates'in tweet['geo'] and tweet['geo']['coordinates']:
                #     with_location = True
                # elif tweet['coordinates'] and 'coordinates' in tweet['coordinates'] 
                #     and tweet['coordinates']['coordinates']:
                #     with_location = True
                # elif tweet['place'] and 'bounding_box' in tweet['place']:

        except tweepy.TweepError as e:
            print(e)
    
    return finish_state
            
def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi",["ifile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i","--ifile"):
            inputfile = arg


if __name__ == "__main__":
#     main(sys.argv[1:])
    # register database
    server = couchdb.Server(db_server)
    print(server)
    db_name = 'tweets_search_by_geocode'
    # db_name = 'test1_tweets_db'
    try:
        if db_name not in server:
            db = server.create(db_name)
        else:
            db = server[db_name]
    except Exception as e:
    # except PreconditionFailed as e:
        command_str = 'curl -X DELETE' + db_server + '/' + db_name
        # os.system(command_str)
        # db = server.create(db_name)
        print(e)
    

    api = generate_api('api-1')
    limit_status = api.rate_limit_status()
    request_left_15min = limit_status['resources']['search']['/search/tweets']['remaining']
    print("request_left_15min:",request_left_15min)

    topic_words = []
    with open("topic_words.txt",'r') as f:
        topic_words = f.read().split('\n')
        topic_words = [w.strip() for w in topic_words]
    f.close()

    for word in topic_words:
        search_tweets(word,api,db)