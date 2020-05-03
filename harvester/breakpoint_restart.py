import json

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