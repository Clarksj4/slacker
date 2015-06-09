def msg_response(response_message, response_code, messages=None):
    r_dict = { 
            "msg_read_response" : {
                "response_message" : response_message,
                "response_code": response_code, },
            "messages": messages,
            }
    return r_dict

def msg_store(response_message, response_code, message_id=0):
    r_dict = {
            "new_msg_response": {
                "response_message" : response_message,
                "response_code" : response_code,
                }
            }
    if (message_id != 0):
        r_dict["new_msg_response"]["message_id"] = message_id
    return r_dict

def msg_delete(response_message, response_code):
    r_dict = {
            "del_response" : {
                "response_message" : response_message,
                "response_code" : response_code,
                },
            }
    return r_dict
