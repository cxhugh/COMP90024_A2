import tweepy, time, twitter_credentials,json,datetime, logging
from tweepy import OAuthHandler
from tweepy import Cursor


def search():
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    count,maxCount = 0,10
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    #topic = ("online learnin OR home schooling OR  education online OR distance learning OR virtual class OR learn at home OR remote learning OR remote teaching OR home schooling OR online tutoring")
    with open('tweets50.json', 'w+') as f:
        while count < maxCount:
            try:
                results = tweepy.Cursor(api.search,
                                    q=('online learning OR home schooling OR education online'),
                                    result_type="recent",
                                    include_entities=True,
                                    geocode="-26.21,135.36,2100km",
                                    lang="en").items()
                for data in results:
                    tmp = []
                    if ('RT @' not in data.text):
                        tmp.append({    
                            'create_time': data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            'id': data.id,
                            'text': data.text,
                            'location': data.user.location,
                            'geo':data.geo,
                            'coordinates':data.coordinates,
                        })
                        json.dump(tmp,f,ensure_ascii=False)
                        f.write('\n')
                count += 1
            except tweepy.RateLimitError as e:
                logging.error(str(e))
            except tweepy.TweepError as e:
                logging.error(str(e))
                break



if __name__ == "__main__":
    search()