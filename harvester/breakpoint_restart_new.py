###################################################################################################################################
##Project: COMP90024--2020S1--Assignment2--Alcohol Tweets and Australian Cities Analytics on the Cloud
##Purpose:  to find out the correlations between alcohol-related tweets and demographic 
##          and behavioural characteristics in Australia cities.
##Team: group05-- Ruiqi Zhu (939162), Zhengyang Li (952972), Jianxin Xu (1014840), Qiuxia YIN (1017231), Fang Qu (1070888)
###################################################################################################################################


import json
import os


def save_searchpoint(user_list, key_group='api-1', max_id=-1):
    max_id = max_id
    filename = 'searchpoint_' + key_group + '.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            prelist = data['user_list']
            users_list = prelist+user_list
        os.remove(filename)
        f.close()
    else:
        users_list = user_list
    state = {"user_list":users_list,"max_id":max_id}
    with open(filename,'w') as f:
        json.dump(state,f)
    f.close()

def save_userpoint(current_user,key_group='api-1'):
    state = {"current_user":current_user}
    filename = 'userpoint_' + key_group + '.json'
    with open(filename,'w') as f:
        json.dump(state,f)
    f.close()  

def get_userlist(key_group='api-1'):
    filename = 'searchpoint_' + key_group + '.json'
    user_list = []
    if os.path.exists(filename):
        with open(filename,'r') as f:
            state = json.load(f)
            user_list = state['user_list']  
    
    return user_list

def get_userpoint(key_group='api-1'):
    filename = 'userpoint_' + key_group + '.json'
    current_user = None
    if os.path.exists(filename):
        with open(filename,'r') as f:
            state = json.load(f)
            current_user = state['current_user']
        f.close()
    return current_user

def clear_breakpoint(key_group):
    filename = 'progress_log' + key_group + '.json'
    if os.path.exists(filename):
        os.remove(filename)
