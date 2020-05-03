from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy,couchdb,json,twitter_credentials,re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



server = "http://admin:admin@172.26.129.233:5984"
local = 'http://admin:admin@localhost:5984'

analyzer = SentimentIntensityAnalyzer()

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
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=topiclist,languages=["en"])

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
            if data['place'] is not None:
                tempPolygon = data['place']['bounding_box']['coordinates'][0]
                centreLatitude = round((tempPolygon[0][1] + tempPolygon[1][1])/2,3)          # round to 3 significant digits
                centreLongitude = round((tempPolygon[1][0] + tempPolygon[2][0])/2,3)         # round to 3 significant digits
                if (centreLatitude <= locationlist[1][0] and centreLatitude >= locationlist[0][0] and
                    centreLongitude <= locationlist[1][1] and centreLongitude >= locationlist[0][1]):      #check if the point is within bounding box
                    tmp_text = data['text']
                    text = re.sub("RT |(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tmp_text)
                    score = analyzer.polarity_scores(text)
                    if data['id_str'] not in db:
                        db.save({
                            '_id': data['id_str'],
                            'text':data['text'],
                            'user_id': data['user']['id_str'],
                            'user_name': data['user']['screen_name'],
                            'sentiment':score,
                            "coordinates": [centreLatitude,centreLongitude]
                        })
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':
 
    topiclist = ['shots', 'booze', 'liquor', 'alcohol','vodka', 'rum', 'beer', 'wine', 'whisky', 'soju',
                  'ginebra', 'baijiu', 'weizenkorn', 'cider', 'mead', 'Saké', 'gin', 'brandy', 'tequila', 'absinthe', 
                  'Radler', 'shochu', 'pastis', 'cynar', 'vermouth', 'Cognac','tipsy', 'drunk', 'turnt', 'hangover', 
                  'blackout','hangover', 'blackout','cocktail', 'Cosmopolitan', 'Tequila Sunrise', 'Moscow Mule',
                  'down the hatch', 'pub crawl', 'bar crawl','DUI', 'DWI', 'the demon drink', 'binge drinking', 'alcoholism', 
                  'drinker', 'alcoholic', 'Dan Murphy', 'bottled spirits', 'bottled liqueur','Mr Black Coffee Liqueur', 'Archie Rose', 
                  'Onyx Coffee Spirits', 'St Agnes', 'Tamborine Mountain Distillery', 'Hippocampus', 'Old Young', 'Four Pillars Navy Strength',
                  'Brookie', 'Noble Cut', 'Never Never Distilling Co.', 'Tooheys', 'Goon', 'Jagerbombs', 'Tamborine Mountain', 'Carlton Draught', 
                  'Carlton Mid', 'Hahn Premium Light', 'Corona Extra', 'Pure Blonde', 'Tooheys New', 'Tooheys Extra Dry',
                  'Penfolds', 'Cape Mentelle', 'Yellow Tail', 'Jacobs Creek', 'Jim Barry', 'Wolf Blass', 'Rockford, hardys', 'wynns coonawarra estate', 'yarra yering', 
                  'vase felix', 'langmeil winery', 'by farr', 'grosset', 'henschke', 'Petaluma', 'chateau tanunda', 'mount mary vineyard', 'mount pleasant', 'yalumba', 
                  'yering station', 'Houghton', 'clonakilla', 'moss wood', 'tapanappa']
    locationlist = [[-44.11,111.87],[-10.64,156.79]] #bottom-left，top-right
    location_list = [111.87,-44.11,156.79,-10.64]

    couch = couchdb.Server(local)
    dbname = "stream_tweets"

    if dbname not in couch:
        db = couch.create(dbname)
    else:
        db = couch[dbname]

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(topiclist,locationlist,location_list)