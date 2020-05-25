from couchdb import design

# australia tweets
# all topic state count
map_function_alltopic_state_count = """function(doc){
    if(doc.state != null && doc.state != "null"){
        emit(doc.state);
    }
}"""

# alcohol state count
map_function_alcohol_state_count = """function(doc){
    if(doc.related == 1){
        if(doc.state != null && doc.state != "null"){
            emit(doc.state);
        }
    }
}"""

# all topic city count
map_function_alltopic_city_count = """function(doc){
locations = {
    "Greater Sydney": [149.9719,-34.3312,151.6305,-32.9961],
    "Greater Melbourne": [144.3336,-38.5030,145.8784,-37.1751],
    "Greater Brisbane":[152.0734,-28.3640,153.5467,-26.4519],
    "Greater Adelaide": [138.4362,-35.3503,139.0440,-34.5002],
    "Greater Perth":[115.4495,-32.8019,116.4151,-31.4551],
    "Greater Hobart": [147.0267,-43.1213,147.9369,-42.6554],
    "Greater Darwin": [130.8151,-12.8619,131.3967,-12.0010],
    "Australian Capital Territory":[148.7628,-35.9208,149.3993,-35.1244]
    };
    
    if(doc.coordinates != null){
        lat = doc.coordinates[0];
        lng = doc.coordinates[1];
        var tweetCity = null;
        for(var city in locations){
            location = locations[city];
            if(location[0] <= lng && lng <= location[2] && location[1]<=lat && lat<=location[3]){
                tweetCity = city;
                break;

            }
        }
    } 

    if(tweetCity!=null){
        emit(tweetCity);
    }
}"""

# alcohol city count
map_function_alcohol_city_count = """function(doc){
locations = {
    "Greater Sydney": [149.9719,-34.3312,151.6305,-32.9961],
    "Greater Melbourne": [144.3336,-38.5030,145.8784,-37.1751],
    "Greater Brisbane":[152.0734,-28.3640,153.5467,-26.4519],
    "Greater Adelaide": [138.4362,-35.3503,139.0440,-34.5002],
    "Greater Perth":[115.4495,-32.8019,116.4151,-31.4551],
    "Greater Hobart": [147.0267,-43.1213,147.9369,-42.6554],
    "Greater Darwin": [130.8151,-12.8619,131.3967,-12.0010],
    "Australian Capital Territory":[148.7628,-35.9208,149.3993,-35.1244]
    };
    
    if(doc.related == 1){
        if(doc.coordinates != null){
            lat = doc.coordinates[0];
            lng = doc.coordinates[1];
            var tweetCity = null;
            for(var city in locations){
                location = locations[city];
                if(location[0] <= lng && lng <= location[2] && location[1]<=lat && lat<=location[3]){
                    tweetCity = city;
                    break;
    
                }
            }
        } 
    
        if(tweetCity!=null){
            emit(tweetCity);
        }
    }
}
"""

# all topic sa2 count
map_function_alltopic_sa2_count = """function(doc){
    if(doc.suburb != -1 && doc.suburb != null){
        emit(doc.suburb);
    }
}"""

# alcohol sa2 count
map_function_alcohol_sa2_count = """function(doc){
    if(doc.related == 1){
        if(doc.suburb != -1 && doc.suburb != null){
            emit(doc.suburb);
        }
    }
}"""


# all topic state sentiment avg
map_function_alltopic_state_senti_avg = """function(doc){
    if(doc.state != null && doc.state != "null"){
        emit(doc.state, doc.compound);
    }
}"""

# alcohol state sentiment avg
map_function_alcohol_state_senti_avg = """function(doc){
    if(doc.related == 1){
        if(doc.state != null && doc.state != "null"){
            emit(doc.state, doc.compound);
        }
    }
}"""


# all topic city sentiment avg
map_function_alltopic_city_senti_avg = """function(doc){
    locations = {
    "Greater Sydney": [149.9719,-34.3312,151.6305,-32.9961],
    "Greater Melbourne": [144.3336,-38.5030,145.8784,-37.1751],
    "Greater Brisbane":[152.0734,-28.3640,153.5467,-26.4519],
    "Greater Adelaide": [138.4362,-35.3503,139.0440,-34.5002],
    "Greater Perth":[115.4495,-32.8019,116.4151,-31.4551],
    "Greater Hobart": [147.0267,-43.1213,147.9369,-42.6554],
    "Greater Darwin": [130.8151,-12.8619,131.3967,-12.0010],
    "Australian Capital Territory":[148.7628,-35.9208,149.3993,-35.1244]
    };
    
    if(doc.coordinates != null){
        lat = doc.coordinates[0];
        lng = doc.coordinates[1];
        var tweetCity = null;
        for(var city in locations){
            location = locations[city];
            if(location[0] <= lng && lng <= location[2] && location[1]<=lat && lat<=location[3]){
                tweetCity = city;
                break;

            }
        }
    } 

    if(tweetCity!=null){
        emit(tweetCity, doc.compound);
    }
}
"""

# alcohol city sentiment avg
map_function_alcohol_city_senti_avg = """function(doc){
         locations = {
        "Greater Sydney": [149.9719,-34.3312,151.6305,-32.9961],
        "Greater Melbourne": [144.3336,-38.5030,145.8784,-37.1751],
        "Greater Brisbane":[152.0734,-28.3640,153.5467,-26.4519],
        "Greater Adelaide": [138.4362,-35.3503,139.0440,-34.5002],
        "Greater Perth":[115.4495,-32.8019,116.4151,-31.4551],
        "Greater Hobart": [147.0267,-43.1213,147.9369,-42.6554],
        "Greater Darwin": [130.8151,-12.8619,131.3967,-12.0010],
        "Australian Capital Territory":[148.7628,-35.9208,149.3993,-35.1244]
        };
        
    if(doc.related == 1){
        if(doc.coordinates != null){
            lat = doc.coordinates[0];
            lng = doc.coordinates[1];
            var tweetCity = null;
            for(var city in locations){
                location = locations[city];
                if(location[0] <= lng && lng <= location[2] && location[1]<=lat && lat<=location[3]){
                    tweetCity = city;
                    break;
    
                }
            }
        } 
    
        if(tweetCity!=null){
            emit(tweetCity, doc.compound);
        }
    }
}"""

# all topic sa2 sentiment avg
map_function_alltopic_sa2_senti_avg = """function(doc){
    if(doc.suburb != -1 && doc.suburb != null){
        emit(doc.suburb, doc.compound);
    }
}"""

# alcohol sa2 sentiment avg
map_function_alcohol_sa2_senti_avg = """function(doc){
    if(doc.related == 1){
        if(doc.suburb != -1 && doc.suburb != null){
            emit(doc.suburb, doc.compound);
        }
    }
}"""


# alcohol state sentiment count
map_function_alcohol_state_senti_count = """function(doc){
    if(doc.related == 1){
        if(doc.state != null){
            emit([doc.state, doc.sentiment]);
        }
    }
}"""

# alcohol city sentiment count
map_function_alcohol_city_senti_count = """function(doc){
locations = {
    "Greater Sydney": [149.9719,-34.3312,151.6305,-32.9961],
    "Greater Melbourne": [144.3336,-38.5030,145.8784,-37.1751],
    "Greater Brisbane":[152.0734,-28.3640,153.5467,-26.4519],
    "Greater Adelaide": [138.4362,-35.3503,139.0440,-34.5002],
    "Greater Perth":[115.4495,-32.8019,116.4151,-31.4551],
    "Greater Hobart": [147.0267,-43.1213,147.9369,-42.6554],
    "Greater Darwin": [130.8151,-12.8619,131.3967,-12.0010],
    "Australian Capital Territory":[148.7628,-35.9208,149.3993,-35.1244]
    };
    
    if(doc.related == 1){
        if(doc.coordinates != null){
            lat = doc.coordinates[0];
            lng = doc.coordinates[1];
            var tweetCity = null;
            for(var city in locations){
                location = locations[city];
                if(location[0] <= lng && lng <= location[2] && location[1]<=lat && lat<=location[3]){
                    tweetCity = city;
                    break;
    
                }
            }
        } 
    
        if(tweetCity!=null){
            emit([tweetCity, doc.sentiment]);
        }
    }
}"""

# alcohol sa2 sentiment count
map_function_alcohol_sa2_senti_count = """function(doc){
    if(doc.related == 1){
        if(doc.suburb != -1 && doc.suburb != null){
            emit([doc.suburb, doc.sentiment]);
        }
    }
}"""

# alcohol australia sentiment count
map_function_alcohol_australia_senti_count = """function(doc){
    location = [96.8168,-43.7405,159.1092,-9.1422];

    if(doc.related == 1){
        if(doc.coordinates != null){
            lat = doc.coordinates[0];
            lng = doc.coordinates[1];
            if(location[0] <= lng && lng <= location[2] && location[1]<=lat && lat<=location[3]){
                emit(doc.sentiment);
            }
        } 
    }
}"""


# alltopic australia hashtag count
map_function_alltopic_australia_hashtag_count = """function(doc){
    location = [96.8168,-43.7405,159.1092,-9.1422];

    if(doc.coordinates != null){
        lat = doc.coordinates[0];
        lng = doc.coordinates[1];
        if(location[0] <= lng && lng <= location[2] && location[1]<=lat && lat<=location[3]){
        
            text = doc.text;
            text.split(" ").forEach(function(x) {
                if(x.indexOf("#") != -1){
                    emit(x);
                }
            });
        }
    }

}"""

# alcohol australia hashtag count
map_function_alcohol_australia_hashtag_count = """function(doc){
    location = [96.8168,-43.7405,159.1092,-9.1422];

    if(doc.related == 1){
        if(doc.coordinates != null){
            lat = doc.coordinates[0];
            lng = doc.coordinates[1];
            if(location[0] <= lng && lng <= location[2] && location[1]<=lat && lat<=location[3]){

                text = doc.text;
                text.split(" ").forEach(function(x) {
                    if(x.indexOf("#") != -1){
                        emit(x);
                    }
                });
            }
        }
    }
}"""

# _sum, _count, _stats
reduce_function_sum = '_sum'

reduce_function_count = '_count'

reduce_function_avg = """function (key, values, rereduce) {
    return sum(values)/values.length;
}"""


def create_view(db, design_name, view_name, map_function, reduce_function):
    view = design.ViewDefinition(design_name, view_name, map_function, reduce_function)
    view.sync(db)





