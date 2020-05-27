###################################################################################################################################
##Project: COMP90024--2020S1--Assignment2--Alcohol Tweets and Australian Cities Analytics on the Cloud
##Purpose:  to find out the correlations between alcohol-related tweets and demographic 
##          and behavioural characteristics in Australia cities.
##Team: group05-- Ruiqi Zhu (939162), Zhengyang Li (952972), Jianxin Xu (1014840), Qiuxia YIN (1017231), Fang Qu (1070888)
###################################################################################################################################

import tweepy
import sys, getopt, os
import couchdb
import json
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from breakpoint_restart_new import save_searchpoint,save_userpoint
from geojson_data.sa2 import get_suburbID_frm_coord, get_stateID_frm_coord
from shapely.geometry import Point
from get_ips import server_address

# CONSTANT
TWEETSPREQUERY = 100 # max for search api
USER_TIMELINE_MAXCOUNT = 200
TOTAL_TWEET_PER_USER = 1000
MAX_TWITTER_NUMS = 200000
# db_server = 'http://lzy:woaideni@127.0.0.1:5984'
db_server = 'http://admin:admin@' + server_address() + ':5984'
db_name = 'australia_tweets'
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

def search_tweets(api,db,geocode,key_group):
    POINT = geocode.split(",")[:2]
    POINT = [float(i) for i in POINT]
    user_list = []
    count = 0
    max_id = -1
    request_times = 0 
    topic_words = get_topic_words() 
    while count<MAX_TWITTER_NUMS:
        try:
            if max_id <= 0:
                # search api returns from big id to small id
                tweets_list = api.search(geocode=geocode,count=TWEETSPREQUERY,
                    tweet_mode="extended")
            else:
                # search start from previous biggest one - 1, avoid redundency
                tweets_list = api.search(geocode=geocode,count=TWEETSPREQUERY,
                    tweet_mode="extended",max_id=str(max_id-1))
            request_times += 1
            if request_times%10 == 0 and request_times<3000:
                save_searchpoint(user_list=user_list,key_group=key_group,max_id=max_id)

                print('send request ',request_times)

            if not tweets_list:
                print("no new twitter found")
                break
            
            max_id = tweets_list[-1].id
            for t in tweets_list:               
                tweet = t._json
                if tweet['id_str'] not in db:                        
                    sub_id, sub_name, coordinates = get_coordinates(tweet)
                    if coordinates is None or not coordinates:
                        coordinates = POINT
                    alcohol_related = 0
                    if is_topic_match(tweet['full_text'],topic_words):
                        alcohol_related = 1
                    sentiment_score = sentiment_analyzer.polarity_scores(tweet['full_text'])
                    filter_tweet_info = {'_id':tweet['id_str'],
                        'text':tweet['full_text'],
                        'user_id':tweet['user']['id_str'],
                        'user_name':tweet['user']['screen_name'],
                        'sentiment':get_sentiment(sentiment_score),
                        'compound':sentiment_score['compound'],
                        'coordinates':coordinates,
                        'location_tag':1,
                        'state':get_stateID_frm_coord(coordinates),
                        'suburb':sub_id,
                        'related':alcohol_related}
                    try:
                        db.save(filter_tweet_info)
                    except Exception as e:
                        print(e)
                        pass 
                    count+=1

                    if tweet['user']['id_str'] not in user_list:
                        user_list.append(tweet['user']['id_str'])
        except tweepy.TweepError as e1:
            print(e1)
    return user_list

def search_tweets_by_user(user_list,api,db,key_group):
    # 100,000 request per day per app 
    # max 3,200 for a single user
    # 1500 per 15 mins
    topic_words = get_topic_words()
    for i,user in enumerate(user_list):
        t_count = 0
        max_id = -1
        test = []
        try:
            while t_count < TOTAL_TWEET_PER_USER:
                if max_id <= 0:
                    tweets_list = api.user_timeline(id=user,count=USER_TIMELINE_MAXCOUNT)
                else:
                    tweets_list = api.user_timeline(id=user,count=USER_TIMELINE_MAXCOUNT,
                        max_id=str(max_id-1))
                if i%10 == 0:
                    save_userpoint(current_user=user,key_group=key_group)
                if not tweets_list:
                    print("no new twitter found")
                    break    
                max_id = tweets_list[-1].id
                t_count += len(tweets_list)

                for t in tweets_list:               
                    tweet = t._json
                    if tweet['id_str'] not in db:
                        sub_id, sub_name, coordinates = get_coordinates(tweet)
                        if coordinates: 
                            alcohol_related = 0
                            if is_topic_match(tweet['text'],topic_words):
                                alcohol_related = 1
                            sentiment_score = sentiment_analyzer.polarity_scores(tweet['text'])
                            filter_tweet_info = {'_id':tweet['id_str'],
                                'text':tweet['text'],
                                'user_id':tweet['user']['id_str'],
                                'user_name':tweet['user']['screen_name'],
                                'sentiment':get_sentiment(sentiment_score),
                                'compound':sentiment_score['compound'],
                                'coordinates':coordinates,
                                'location_tag':1,
                                'state':get_stateID_frm_coord(coordinates),
                                'suburb':sub_id,
                                'related':alcohol_related}
                            try:
                                db.save(filter_tweet_info) 
                            except Exception as e1:
                                print(e1)
                                pass                        
        except Exception as e:
            print(e)

def get_coordinates(tweet):
    # tweet must be json format
    coordinates = None
    suburb_id = -1
    suburb_name = "null"
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
    
    if coordinates:
        point = Point(coordinates[1],coordinates[0])
        suburb_id, suburb_name = get_suburbID_frm_coord(point)
    return suburb_id, suburb_name, coordinates

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
        print(e)
    except Exception as e:
        command_str = 'curl -X DELETE' + db_server + '/' + db_name
        os.system(command_str)
        db = server.create(db_name)
        print(e)
    
    return db

def get_topic_words(for_timeline=True):
    topic_words = []
    with open("topic_words.txt",'r') as f:
        topic_words = f.read().split(',')
        topic_words = [w.strip() for w in topic_words]
    f.close()    
    if for_timeline:
        topic_words = [" "+w.lower() for w in topic_words]   
    
    return topic_words

def get_sentiment(score):
    # get the sentiment of tweets by vadar compound results
    compound = score['compound']
    if compound > 0.05:
        return 'pos'
    elif compound < 0.05:
        return 'neg'
    else:
        return 'neu'