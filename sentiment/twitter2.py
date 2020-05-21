from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy,couchdb,json,twitter_credentials2,re,time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib3.exceptions import ProtocolError
from http.client import IncompleteRead as http_incompleteRead
from urllib3.exceptions import IncompleteRead as urllib3_incompleteRead

from shapely.geometry import Point, shape



server = "http://admin:admin@172.26.129.233:5984"
local = 'http://admin:admin@localhost:5984'

analyzer = SentimentIntensityAnalyzer()


def get_suburbID_frm_coord(point):
    suburb_id = -1
    for item in js['features']:
        if item['geometry'] != None:
            polygon = shape(item['geometry'])
            if polygon.contains(point):
                suburb_id = item['properties']['SA2_MAIN16']
                break
    return suburb_id

def get_state_frm_coord(point):
    state_name = None
    for item in js2['features']:
        if item['geometry'] != None:
            polygon = shape(item['geometry'])
            if polygon.contains(point):
                state_name = item['properties']['STATE_NAME']
                break
    return state_name

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self,topiclist,locationlist,location_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(locationlist)
        auth = OAuthHandler(twitter_credentials2.CONSUMER_KEY, twitter_credentials2.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials2.ACCESS_TOKEN, twitter_credentials2.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        while True:
            try:
                stream.filter(locations=location_list,languages=["en"])
            except (ProtocolError, AttributeError):
                continue

# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self,locationlist):
        self.locationlist=locationlist

    def on_data(self, data):
        try:
            data = json.loads(data)
            tmp_text = data['text']
            text = re.sub("RT |(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tmp_text)
            score = analyzer.polarity_scores(text)
            sentiment=0
            if score['compound'] >= 0.5:
                sentiment = 'pos'
            elif score['compound'] >= -0.5 and score['compound'] < 0.5:
                sentiment = 'neu'
            else:
                sentiment = 'neg'
                
            if data['place'] is not None:
                tempPolygon = data['place']['bounding_box']['coordinates'][0]
                centreLatitude = round((tempPolygon[0][1] + tempPolygon[1][1])/2,3)          # round to 3 significant digits
                centreLongitude = round((tempPolygon[1][0] + tempPolygon[2][0])/2,3)         # round to 3 significant digits
                if (centreLatitude <= locationlist[1][0] and centreLatitude >= locationlist[0][0] and
                    centreLongitude <= locationlist[1][1] and centreLongitude >= locationlist[0][1]):      #check if the point is within bounding box
                    coordinate = [centreLatitude,centreLongitude]
                    point = Point(coordinate[1],coordinate[0])
                    state = get_state_frm_coord(point)
                    if state == 'Victoria':
                        suburb = get_suburbID_frm_coord(point)
                    else:
                        suburb = None
                    if data['id_str'] not in db:
                        db.save({
                            '_id': data['id_str'],
                            'text':data['text'],
                            'user_id': data['user']['id_str'],
                            'user_name': data['user']['screen_name'],
                            'sentiment':sentiment,
                            'compound':score['compound'],
                            "coordinates": [centreLatitude,centreLongitude],
                            'location_tag':1,
                            'state':state,
                            'suburb':suburb,
                            'related':0
                        })
                else:
                    if data['id_str'] not in db:
                        db.save({
                            '_id': data['id_str'],
                            'text':data['text'],
                            'user_id': data['user']['id_str'],
                            'user_name': data['user']['screen_name'],
                            'sentiment':sentiment,
                            'compound':score['compound'],
                            "coordinates": [centreLatitude,centreLongitude],
                            'location_tag':0,
                            'state': None,
                            'suburb': None,
                            'related': 0
                        })
            else:
                pass
        
        except http_incompleteRead as e:
            print("http.client Incomplete Read error: %s" % str(e))
            print("~~~ Restarting stream search in 5 seconds... ~~~")
            time.sleep(5)
            #restart stream - simple as return true just like previous exception?
            return True
        except urllib3_incompleteRead as e:
            print("urllib3 Incomplete Read error: %s" % str(e))
            print("~~~ Restarting stream search in 5 seconds... ~~~")
            time.sleep(5)
            return True
        except BaseException as e:
            print("Error on_data: %s, Pausing..." % str(e))
            time.sleep(5)
            return True
        return True
          

    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':
 
    topiclist = []
    locationlist = [[-44.11,111.87],[-10.64,156.79]] #bottom-left，top-right
    location_list = [111.87,-44.11,156.79,-10.64]

    couch = couchdb.Server(server)
    dbname = "australia_tweets"

    if dbname not in couch:
        db = couch.create(dbname)
    else:
        db = couch[dbname]
    with open("SA2_2016_AUST_GreaterMelb.json") as f:
        js = json.load(f)
    with open("states.json") as f:
        js2 = json.load(f)

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(topiclist,locationlist,location_list)