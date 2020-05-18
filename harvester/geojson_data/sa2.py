import json
from shapely.geometry import Point, shape

with open("./geojson_data/SA2_2016_AUST_GreaterMelb.json") as f:
    js = json.load(f)

with open("./geojson_data/states.json") as f1:
    js1 = json.load(f1)

def get_stateID_frm_coord(coordinate):
    point = Point(coordinate[1],coordinate[0])
    state_name = "null"
    for item in js1['features']:
        if item['geometry'] != None:
            polygon = shape(item['geometry'])
            if polygon.contains(point):
                state_name = item['properties']['STATE_NAME']
                break
    return state_name

def get_stateID_frm_coord(coordinate):
    point = Point(float(coordinate[1]),float(coordinate[0]))
    state_id = -1
    state_name = "null"
    for item in js1['features']:
        if item['geometry'] != None:
            polygon = shape(item['geometry'])
            if polygon.contains(point):
                # state_name = item['properties']['STE_NAME16']
                state_name = item['properties']['STATE_NAME']
                break
    return state_name

def get_suburbID_frm_coord(point):
    suburb_id = -1
    suburb_name = "null"
    for item in js['features']:
        if item['geometry'] != None:
            polygon = shape(item['geometry'])
            if polygon.contains(point):
                suburb_id = item['properties']['SA2_MAIN16']
                suburb_name = item['properties']['SA2_NAME16']
                break
    return suburb_id, suburb_name

# test
# coordinate = [-37.973,145.053]
# # Point前面是经度，后面是维度
# point = Point(coordinate[1],coordinate[0])
# state_name = get_stateID_frm_coord(coordinate)
# print("state:",state_name)

# suburb_id, suburb_name = get_suburbID_frm_coord(point)
# print(suburb_id, suburb_name)


def get_suburbID_frm_place(place):
    place_polygon = shape(place['bounding_box'])
    max_area = 0
    max_area_sub_id = -1
    sub_name = "null"

    for item in js['features']:
        if item['geometry'] != None:
            suburb_polygon = shape(item['geometry'])
            if place_polygon.intersects(suburb_polygon):
                area = place_polygon.intersection(suburb_polygon).area
                if area > max_area:
                    max_area = area
                    max_area_sub_id = item['properties']['SA2_MAIN16']
                    sub_name = item['properties']['SA2_NAME16']
    return max_area_sub_id, sub_name

# test
# place= {
#     "url": "https://api.twitter.com/1.1/geo/id/00c262dc7a56fb4e.json",
#     "place_type": "city",
#     "country_code": "AU",
#     "id": "00c262dc7a56fb4e",
#     "bounding_box": {
#         "type": "Polygon",
#         "coordinates": [
#             [
#                 [
#                     145.650457088,
#                     -17.038658997
#                 ],
#                 [
#                     145.783431648,
#                     -17.038658997
#                 ],
#                 [
#                     145.783431648,
#                     -16.7223939305
#                 ],
#                 [
#                     145.650457088,
#                     -16.7223939305
#                 ]
#             ]
#         ]
#     },
#     "full_name": "Cairns, Queensland",
#     "country": "Australia",
#     "contained_within": [],
#     "attributes": {},
#     "name": "Cairns"
# }

# suburb_id, suburb_name = get_suburbID_frm_place(place)
# print(suburb_id,suburb_name)
