__author__ = 'alexmcneill'

def add_channel_response(response_message, response_code):
    response_dict = {"new_channel_response": {"response_message": response_message, "response_code": response_code}}
    return response_dict

def read_channel_response(response_message, response_code, channel = None):
    response_dict = {"channel_read_response": {"response_message": response_message, "response_code": response_code}}

    if channel is not None:
        response_dict["channel"] = channel
    return response_dict

def delete_channel_response(response_message, response_code,):
    response_dict = {"new_channel_response": {"response_message": response_message, "response_code": response_code}}
    return response_dict
