import json,logging,tweepy,couchdb,twitter_credentials,re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy import OAuthHandler
from tweepy import Cursor

server = "http://admin:admin@172.26.129.233:5984"
local = 'http://admin:admin@localhost:5984'

analyzer = SentimentIntensityAnalyzer()

geolocation=['-26.21,135.36']

def search(count,maxCount):
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    while count < maxCount:
        try:
            results = tweepy.Cursor(api.search,
                                    q=('online learning OR home schooling OR education online'),
                                    result_type="recent",
                                    include_entities=True,
                                    geocode="-26.21,135.36,2100km",
                                    lang="en").items()
            for tweet in results:
                if ('RT @' not in tweet.text):
                    item = tweet._json
                    tmp_text = item['text']
                    text = re.sub("RT |(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tmp_text)
                    score = analyzer.polarity_scores(text)
                    if item['id_str'] not in db:
                        db.save({
                            'id':item['id_str'],
                            'user':{
                                'name':item['user']['name'],
                                'screen_name':item['user']['screen_name'],
                                'location':item['user']['location'],
                                'description':item['user']['description'],
                            },
                            'tweet_info':{
                                'text':item['text'],
                                'created_at':item['created_at'],
                                'sentiment':score,
                                'compound_score':score['compound'],
                                'cleaned_text':text,
                                'retweet_count': item['retweet_count'], 
                                'favorite_count': item['favorite_count']
                            },
                            "coordinates": item["coordinates"]["coordinates"] if item["coordinates"] else geolocation
                        })
        except tweepy.RateLimitError as e:
                logging.error(str(e))
        except tweepy.TweepError as e:
                logging.error(str(e))
                break
    return results




if __name__ == "__main__":
    couch = couchdb.Server(server)
    dbname = "search_tweets"

    if dbname not in couch:
        db = couch.create(dbname)
    else:
        db = couch[dbname]
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    count,maxCount = 0,5
    while True:
        data = search(count,maxCount)
    print("finished")
    