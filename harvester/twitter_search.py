import tweepy
import sys, getopt
import couchdb
# import mpi4py
# import json

key_group = 1
if key_group == 1:
    consumer_key = "joDtmea4C6IhoObFF2TQ7PwtQ"
    consumer_secret = "Om0ihdmlITqX5E5TUwec86ePmEkra2pfWjdwfe2rsbZKAqbxII"
    access_token = "1251764501663244288-uYSaMzoDD450mpWAhzD3O1D2zoCt7s"
    access_token_secret = "BC7huQo17vhFdZpFDEiaa0jVuxYrq5oowxZp0kVDiGtId"
elif key_group == 2:
    consumer_key = "iSFYtYVuduON726ZCwIBbCpBQ"
    consumer_secret = "8XJsHwQ4pDE0vWiUAKBrLt5T2T3lFSc23ciZs4aTfOXOz6bLvH"
    access_token = "1251764501663244288-rRfSsesuwlTpBR489qcc429XSQGWlv"
    access_token_secret = "CrPInVlCHm9ThXbUgweyVgCxOWye07ltOiVngBnn0kx5B"
elif key_group == 3:
    consumer_key = "a20YmLNujGO8FPPpT6o00TdxY"
    consumer_secret = "W0mn8pfDekIax69u4uo4LD22g5ss6TiWUardjbfKHN3IGyutG2"
    access_token = "1251764501663244288-YT8QM9sOuRIpz8kVEVdIFZ7TFt3NXA"
    access_token_secret = "pjxhhbsnEfivPNp6pHKdGLSHmuVAVd8hMdA86oXtjB2ex"


db_server = 'http://lzy:woaideni@127.0.0.1:5984'

# register database
# def register_db(db_server):
server = couchdb.Server(db_server)
try:
    db = server.create('tweets_mel_elearning')
except Exception as e:
    print(e)
    db = server['tweets_mel_elearning']

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

limit_status = api.rate_limit_status()
request_left_15min = limit_status['resources']['search']['/search/tweets']['remaining']
print("request_left_15min:",request_left_15min)

TWEETSPREQUERY = 100 # max
geocode_mel = "-37.813629,144.963058,80km"

q_or=('online learning OR home schooling OR education online')
key_words = ["distance learning","elearning","online-learning"]

def search_tweets(query):
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

                filter_tweet_info = {'_id':tweet['id_str'],'created_at':tweet['created_at'],'text':tweet['full_text'],
                    'user':tweet['user'],'geo':tweet['geo'],'coordinates':tweet['coordinates'],'place':tweet['place']}
                if 'location' in tweet:
                    print(tweet['location'])

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
            

search_tweets()


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

# if __name__ == "__main__":
#     main(sys.argv[1:])