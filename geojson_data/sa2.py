import json
from shapely.geometry import Point, shape


with open("SA2_2016_AUST_VIC.json") as f:
    js = json.load(f)


#print(json.dumps(data['features'][51], indent=4, sort_keys=True))


def get_suburbID_frm_coord(point):
    suburb_id = -1
    for item in js['features']:
        if item['geometry'] != None:
            polygon = shape(item['geometry'])
            if polygon.contains(point):
                suburb_id = item['properties']['SA2_MAIN16']
                break
    return suburb_id


coordinate = [140.999474522999, -37.5050599967256]
#coordinate = [115.617614368,-32.675715325]

point = Point(coordinate[0],coordinate[1])
suburb_id = get_suburbID_frm_coord(point)
print(suburb_id)


def get_suburbID_frm_place(place):
    place_polygon = shape(place['bounding_box'])
    max_area = 0
    max_area_sub_id = -1

    for item in js['features']:
        if item['geometry'] != None:
            suburb_polygon = shape(item['geometry'])
            if place_polygon.intersects(suburb_polygon):
                area = place_polygon.intersection(suburb_polygon).area
                if area > max_area:
                    max_area = area
                    max_area_sub_id = item['properties']['STE_NAME16']
    return max_area_sub_id

place= {
    "url": "https://api.twitter.com/1.1/geo/id/00c262dc7a56fb4e.json",
    "place_type": "city",
    "country_code": "AU",
    "id": "00c262dc7a56fb4e",
    "bounding_box": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    145.650457088,
                    -17.038658997
                ],
                [
                    145.783431648,
                    -17.038658997
                ],
                [
                    145.783431648,
                    -16.7223939305
                ],
                [
                    145.650457088,
                    -16.7223939305
                ]
            ]
        ]
    },
    "full_name": "Cairns, Queensland",
    "country": "Australia",
    "contained_within": [],
    "attributes": {},
    "name": "Cairns"
}

suburb_id = get_suburbID_frm_place(place)
print(suburb_id)