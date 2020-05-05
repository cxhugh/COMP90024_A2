import sys, getopt
import json
import twitter_search
from breakpoint_restart import get_breakPoint,clear_breakpoint

def search_harvesrter_run(key_group,geocode,db):
    api = twitter_search.generate_api(key_group)
    twitter_search.get_account_status(api)
    topic_words = twitter_search.get_topic_words()
    # recover from break point
    cur_user, cur_word, user_list, topic_finish = get_breakPoint(key_group=key_group)
    print("breakpoint:(cur_user:",cur_user,",cur_word:",cur_word,",topic_finish:",topic_finish,")")

    #search by key_words and location
    if not topic_finish:
        if cur_word:
            try:
                w = topic_words.index(cur_word)
                topic_words = topic_words[w:]
            except Exception as e:
                pass
        # for word in topic_words:
        user_list += twitter_search.search_tweets(topic_words,api,db,geocode,key_group)

    #search by user 
    topic_words = twitter_search.get_topic_words(for_timeline=True)
    if cur_user:
        try:
            u = user_list.index(cur_user)
            user_list = user_list[u:]
        except Exception as e:
            pass
    twitter_search.search_tweets_by_user(user_list=user_list,api=api,db=db,topic_words=topic_words,
        key_group=key_group)
    clear_breakpoint(key_group)

def main(argv):
    api = ''
    try:
        opts, args = getopt.getopt(argv,"ha:",["api="])
    except getopt.GetoptError:
        print('searchapi_controller.py -a <key-group>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('searchapi_controller.py -a <key-group>')
            sys.exit()
        elif opt in ("-a","--api"):
            api = arg
    
    return api


if __name__ == "__main__":
    key_group = main(sys.argv[1:])

    db = twitter_search.register_database()
    with open("geocode.json",'r') as f:
        location_dict = json.load(f)
    
    number_of_Apis = 3
    for i,geocode in enumerate(location_dict.values()):
        if i%number_of_Apis == (int(key_group[-1])-1):
            # print(i,geocode)
            search_harvesrter_run(key_group,geocode,db)  

