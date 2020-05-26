import couchdb
import json
from math import cos, sin, atan2, sqrt, pi ,radians, degrees
import sys
sys.path.append("../")
from harvester.get_ips import server_address

server =  'http://admin:admin@' + server_address() + ':5984'
#local = "http://127.0.0.1:5984/"

couch = couchdb.Server(server)
database_name = "view_results(australia_tweets)"

try:
    db = couch[database_name]
except couchdb.http.ResourceNotFound:
    db = couch.create(database_name)

def center_geolocation(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)
    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)
    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))

def get_centerpoint(lis):
    area = 0.0
    x,y = 0.0,0.0
 
    a = len(lis)
    for i in range(a):
        lat = lis[i][0] 
        lng = lis[i][1] 
 
        if i == 0:
            lat1 = lis[-1][0]
            lng1 = lis[-1][1]
 
        else:
            lat1 = lis[i-1][0]
            lng1 = lis[i-1][1]
 
        fg = (lat*lng1 - lng*lat1)/2.0
 
        area += fg
        x += fg*(lat+lat1)/3.0
        y += fg*(lng+lng1)/3.0
 
    x = x/area
    y = y/area
 
    return (x,y)

# This is the a function used to save formated center point of each Melbourne suburb and cooresponding
# tweets sentiment to couchdb for leaflet map view 
def main(geojson,point_sent):
    data = db['sa2_alcohol_senti_avg']
    for i in data['rows']:
        # print(i)
        for item in geojson['features']:
            # print(i['key'],item['properties']['SA2_MAIN16'])
            if i['key'] == item['properties']['SA2_MAIN16']:
                locations = item['geometry']['coordinates'][0]
                try:
                    center_point = get_centerpoint(locations)
                    # print(center_point[0])
                    p = [center_point[1],center_point[0]]
                    print(p)
                    point_sent[i['key']] = {"center":p,"value":i['value']}
                except Exception as e:
                    print(e)
                    pass
                break
            
    point_sent['_id'] = "sa2_sentiment_with_point" 
    db.save(point_sent) 

if __name__ == "__main__":
    point_sent = {}
    suburb_info = {}
    file = open("../geojson_data/SA2_2016_AUST_GreaterMelb.json", encoding='utf8').read()
    geojson = json.loads(file)
    suburb_info['_id'] = "suburb_info"
    for item in geojson['features']:
        suburb_info[item['properties']['SA2_MAIN16']] = item['properties']['SA2_NAME16']
    # db.save(suburb_info)
    
        # if i['key'] == item['properties']['SA2_MAIN16']:
    main(geojson,point_sent)


    
   
     
