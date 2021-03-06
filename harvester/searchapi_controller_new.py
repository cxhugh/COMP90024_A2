###################################################################################################################################
##Project: COMP90024--2020S1--Assignment2--Alcohol Tweets and Australian Cities Analytics on the Cloud
##Purpose:  to find out the correlations between alcohol-related tweets and demographic 
##          and behavioural characteristics in Australia cities.
##Team: group05-- Ruiqi Zhu (939162), Zhengyang Li (952972), Jianxin Xu (1014840), Qiuxia YIN (1017231), Fang Qu (1070888)
###################################################################################################################################

import sys, getopt
import json
import twitter_search_new
import breakpoint_restart_new 
from mpi4py import MPI
import time


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
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    db = twitter_search_new.register_database()
    api = twitter_search_new.generate_api(key_group)
    twitter_search_new.get_account_status(api)

    if rank == 0:
        print(" I m rank 0")
        with open("geocode.json",'r') as f:
            location_dict = json.load(f)
        number_of_Apis = 3
        for i,geocode in enumerate(location_dict.values()):
            if i%number_of_Apis == (int(key_group[-1])-1):
                #search by location
                twitter_search_new.search_tweets(api,db,geocode,key_group)  
    else:
        #search by user
        print(" I m rank 1") 
        while True:
            time.sleep(30)
            curr_user = breakpoint_restart_new.get_userpoint(key_group=key_group)
            user_list = breakpoint_restart_new.get_userlist(key_group=key_group)
            try:
                u = user_list.index(curr_user)
                user_list = user_list[u:]
            except Exception as e:
                print(e)
            print("length of userlist:",len(user_list))
            twitter_search_new.search_tweets_by_user(user_list=user_list,api=api,db=db,key_group=key_group)
        


