import tweepy
import sys, getopt, os
import couchdb
import json
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from breakpoint_restart import save_point,get_breakPoint

# CONSTANT
TWEETSPREQUERY = 100 # max for search api
USER_TIMELINE_MAXCOUNT = 200
TOTAL_TWEET_PER_USER = 400
# db_server = 'http://lzy:woaideni@127.0.0.1:5984'
db_server = 'http://admin:admin@172.26.129.233:5984'
db_name = 'alcohol_search'
sentiment_analyzer = SentimentIntensityAnalyzer()

def generate_api(key_group):
    with open('api_keys.json','r') as f:
        keys = f.read()
        keys = json.loads(keys)
    f.close()    
    
    # if key_group == "api-1":
    consumer_key = keys[key_group]['consumer_key']
    consumer_secret = keys[key_group]['consumer_secret']
    access_token = keys[key_group]['access_token']
    access_token_secret = keys[key_group]['access_token_secret']

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

def search_tweets(query_list,api,db,geocode,key_group):
    POINT = geocode.split(",")[:2]
    POINT = [float(i) for i in POINT]
    user_list = []
    for query in query_list:
        sinceId = None
        max_id = -1
        request_times = 0  
        save_point(topic_finish=False,current_word=query,user_list=user_list,key_group=key_group)
        while True:
            try:
                if max_id <= 0:
                    # search api returns from big id to small id
                    tweets_list = api.search(q=query,geocode=geocode,count=TWEETSPREQUERY,
                        tweet_mode="extended")
                else:
                    # search start from previous biggest one - 1, avoid redundency
                    tweets_list = api.search(q=query,geocode=geocode,count=TWEETSPREQUERY,
                        tweet_mode="extended",max_id=str(max_id-1))
                request_times += 1
                print('send request ',request_times)

                if not tweets_list:
                    print("no new twitter found")
                    break
                
                max_id = tweets_list[-1].id
                for t in tweets_list:               
                    tweet = t._json
                    if tweet['id_str'] not in db:                        
                        # coordinates = [-37.813629,144.963058]
                        coordinates = get_coordinates(tweet)
                        if coordinates is None or not coordinates:
                            coordinates = POINT
                        
                        sentiment_score = sentiment_analyzer.polarity_scores(tweet['full_text'])
                        filter_tweet_info = {'_id':tweet['id_str'],
                            'text':tweet['full_text'],
                            'user_id':tweet['user']['id_str'],
                            'user_name':tweet['user']['screen_name'],
                            'sentiment':sentiment_score,
                            'coordinates':coordinates}
                        db.save(filter_tweet_info)

                        if tweet['user']['id_str'] not in user_list:
                            user_list.append(tweet['user']['id_str'])

            except tweepy.TweepError as e:
                print(e)
    return user_list

def search_tweets_by_user(user_list,api,db,topic_words,key_group):
    # 100,000 request per day per app 
    # max 3,200 for a single user
    # 1500 per 15 mins
    for i,user in enumerate(user_list):
        if i%10 == 0:
            save_point(topic_finish=True,current_user=user,user_list=user_list,key_group=key_group)  
        t_count = 0
        sinceId = None
        max_id = -1
        test = []
        try:
            while t_count < TOTAL_TWEET_PER_USER:
                if max_id <= 0:
                    tweets_list = api.user_timeline(id=user,count=USER_TIMELINE_MAXCOUNT)
                else:
                    tweets_list = api.user_timeline(id=user,count=USER_TIMELINE_MAXCOUNT,
                        max_id=str(max_id-1))

                if not tweets_list:
                    print("no new twitter found")
                    break    
                max_id = tweets_list[-1].id
                t_count += len(tweets_list)

                for t in tweets_list:               
                    tweet = t._json
                    if tweet['id_str'] not in db:
                        coordinates = get_coordinates(tweet)
                        if coordinates:
                            if is_topic_match(tweet['text'],topic_words=topic_words):
                                sentiment_score = sentiment_analyzer.polarity_scores(tweet['text'])
                                filter_tweet_info = {'_id':tweet['id_str'],
                                    'text':tweet['text'],
                                    'user_id':tweet['user']['id_str'],
                                    'user_name':tweet['user']['screen_name'],
                                    'sentiment':sentiment_score,
                                    'coordinates':coordinates}
                                db.save(filter_tweet_info)
                                print(filter_tweet_info)                            
        except Exception as e:
            print(e)

def get_coordinates(tweet):
    # tweet must be json format
    coordinates = None
    if tweet['geo'] and 'coordinates'in tweet['geo'] and tweet['geo']['coordinates']:
        coordinates = tweet['geo']['coordinates']
    elif (tweet['coordinates'] and 'coordinates' in tweet['coordinates'] and 
            tweet['coordinates']['coordinates']):
        coordinates = [tweet['coordinates']['coordinates'][1],tweet['coordinates']['coordinates'][0]]
    elif (tweet['place'] and 'bounding_box' in tweet['place'] and 
            'coordinates' in tweet['place']['bounding_box'] and 
            tweet['place']['bounding_box']['coordinates']):
        point = tweet['place']['bounding_box']['coordinates'][0]
        latitude = (point[0][1] + point[1][1])/2
        longitude = (point[0][0] + point[2][0])/2
        coordinates = [latitude,longitude]
    
    return coordinates

def is_topic_match(text,topic_words):
    for w in topic_words:
        if w in text.lower():
            return True
    return False

def get_account_status(api):
    limit_status = api.rate_limit_status()
    request_left_15min = limit_status['resources']['search']['/search/tweets']['remaining']
    user_timeline_left = limit_status['resources']['statuses']['/statuses/user_timeline']['remaining']
    print("search left:",request_left_15min," timeline_left:",user_timeline_left)

def register_database():
    server = couchdb.Server(db_server)
    try:
        if db_name not in server:
            db = server.create(db_name)
        else:
            db = server[db_name]
    except couchdb.PreconditionFailed as e:
        db = server[db_name]
        print(e)
    except Exception as e:
        command_str = 'curl -X DELETE' + db_server + '/' + db_name
        os.system(command_str)
        db = server.create(db_name)
        print(e)
    
    return db

def get_topic_words(for_timeline=False):
    topic_words = []
    with open("topic_words.txt",'r') as f:
        topic_words = f.read().split(',')
        topic_words = [w.strip() for w in topic_words]
    f.close()    
    if for_timeline:
        topic_words = [" "+w.lower() for w in topic_words]   
    
    return topic_words