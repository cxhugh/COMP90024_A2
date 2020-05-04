import json
import os

def save_point(topic_finish,user_list,current_word=None,current_user=None,max_id=None):
    user_list = user_list
    if not topic_finish:
        current_topic_word = current_word
        max_id = max_id
        state = {"topic_finish":topic_finish,"current_word":current_word,
            "max_id":max_id,"user_list":user_list}
    else:
        state = {"topic_finish":topic_finish,"current_user":current_user,
            "user_list":user_list,"max_id":max_id}
    with open("progress_log.json",'w') as f:
        json.dump(state,f)
    f.close()


def get_breakPoint():
    topic_finish = False
    cur_topic_word = None
    cur_user = None
    user_list = []
    if os.path.exists("progress_log.json"):
        with open("progress_log.json",'r') as f:
            state = json.load(f)
            user_list = state['user_list']   
            topic_finish = state['topic_finish']          
            if not topic_finish:
                cur_topic_word = state['current_word']          
            else:
                cur_user = state['current_user']  
        f.close()
    
    return cur_user, cur_topic_word, user_list, topic_finish