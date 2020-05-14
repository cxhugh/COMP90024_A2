import json
import os

def save_point(topic_finish,user_list,key_group='api-1',current_word=None,current_user=None,max_id=-1):
    user_list = user_list
    if not topic_finish:
        current_topic_word = current_word
        max_id = max_id
        state = {"topic_finish":topic_finish,"current_word":current_word,
            "max_id":max_id,"user_list":user_list}
    else:
        state = {"topic_finish":topic_finish,"current_user":current_user,
            "user_list":user_list,"max_id":max_id}
    filename = 'progress_log' + key_group + '.json'
    with open(filename,'w') as f:
        json.dump(state,f)
    f.close()

def get_breakPoint(key_group='api-1'):
    topic_finish = False
    cur_topic_word = None
    cur_user = None
    user_list = []
    filename = 'progress_log' + key_group + '.json'
    if os.path.exists(filename):
        with open(filename,'r') as f:
            state = json.load(f)
            user_list = state['user_list']   
            topic_finish = state['topic_finish']  
            try:        
                if not topic_finish:
                    cur_topic_word = state['current_word']          
                else:
                    cur_user = state['current_user']  
            except Exception as e:
                print(e)
                pass
        f.close()
    
    return cur_user, cur_topic_word, user_list, topic_finish

def clear_breakpoint(key_group):
    filename = 'progress_log' + key_group + '.json'
    if os.path.exists(filename):
        os.remove(filename)