__author__ = 'clarksj4 & camertp1'

import requests
from requests import ConnectionError
import cherrypy
import json
import sys
lib_path = '..'
sys.path.append(lib_path)
from slacker_config import urls


class MessageWriterService:
    """ Facilitates communication between the UI, authorisation service, and message service (channel service).
    MessageWriterService handles a post request by asking the authorisation service to validate a session key and return
    the associated user id. This user id along with the posted message body, and channel id are sent via post request to
    the message service.
    Post requests made to the message writer service return appropriate error / success messages. All request data is in
    json format.
    """
    heads = {'Content-Type': 'application/json'}
    exposed = True

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        """ Handles the posting and authorisation of messages en route to the message service. Takes a new message
        request; asks authorisation service to validate and convert session_id to a user_id; posts user_id, channel_id,
        and message_body to message service.
        Messages posted to this service must be valid json formatted in the following manner:
        {
            "message":
            {
                "channel_id": 0,
                "session_key": 0,
                "body": "Hello World.",
            }
        }
        :return: json data describing the success or failure of the POST request. A write failure will occur when the
        posted json data is missing a parameter(s), or when the authorisation or message services return an error.
        """

        # get the post request data sent to this service. Post data comes in json format.
        post_data = cherrypy.request.json

        try:
            # attempt to extract variables from json data. If the json is not in the correct format (i.e. a parameter
            # is missing) a KeyError exception will be thrown. If the post data is not valid json a TypeError will be
            # thrown.
            session_key = post_data['message']['session_key']
            channel_id = post_data['message']['channel_id']
            message_body = post_data['message']['body']
        except TypeError:
            return {"new_msg_response": {
                "response_message": "Invalid POST request: post data did not contain valid json",
                "response_code": 31}}
        except KeyError:
            return {"new_msg_response": {
                "response_message": "Invalid POST request: post data was missing parameter(s)",
                "response_code": 32}}
        try:
            # attempt to authorize the given session key and get a corresponding user id. In the event of being unable
            # to connect to the authorisation service a ConnectionError will be thrown.
            authorisation_service_response = self._authorize(session_key)
        except ConnectionError:
            return {"new_msg_response": {
                "response_message": "ConnectionError: unable to connect to authorisation service",
                "response_code": 33}}

        try:
            # attempt to extract user_id from returned response. If the authorisation request failed no user_id will be
            # present in response message and a KeyError exception will be thrown.
            user_id = authorisation_service_response['user_id']
        except KeyError:
            return {"new_msg_response": {
                "response_message": "Invalid session key: authorisation failed",
                "response_code": 34}}

        try:
            # attempt to post message to message_service. In the even of being unable to connect to the message service
            # a ConnectionError will be thrown.
            message_service_response = self._write(channel_id, user_id, message_body)
        except ConnectionError:
            return {"new_msg_response": {
                "response_message": "ConnectionError: unable to connect to message service",
                "response_code": 35}}

        # message service response will contain success or failure information.
        return message_service_response

    def _authorize(self, session_key):
        """ Asks authorisation service to validate a session key. If key is valid, authorisation service will return
        corresponding user id.
        :param session_key: the session key to validate
        :return: json data describing the success or failure of the POST request. On success, the json data will contain
        a valid user id corresponding to the given session id. On failure, the json data will contain an error message.
        """
        session_key_json = {'session_key': session_key}
        authorisation_service_url = str(urls.url['auth']) + ":" + str(urls.port['auth'])

        # posts session key json data to authorisation service and returns response. Authorisation service response will
        # be json data containing either an error message or a user id.
        return requests.post(authorisation_service_url,
                             headers=MessageWriterService.heads,
                             data=json.dumps(session_key_json)).json()

    def _write(self, channel_id, user_id, message_body):
        """ Posts a message to message service.
        :param channel_id: the id of the channel in which the message is being posted
        :param user_id: the id of the user who is posting the message
        :param message_body: the contents of the message being posted
        :return: json data describing the success or failure of the POST request.
        """
        new_message_json = {'new_msg': {'channel_id': channel_id, 'user_id': user_id, 'message_string': message_body}}
        message_service_url = urls.url['channels'] + ':' + urls.port['channels']

        # posts new message json data to message service and returns response. Message service response will be json
        # data containing a success or failure message and associated error code.
        return requests.post(message_service_url,
                             headers=MessageWriterService.heads,
                             data=json.dumps(new_message_json)).json()

if __name__ == '__main__':
    conf = {
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
              'tools.response_headers.on': True,
              'tools.response_headers.headers': [('Content-Type',
                                                  'application/json')]}}
    cherrypy.config.update({'server.socket_port': urls.port['msg_writer']})
    cherrypy.quickstart(MessageWriterService(), '/', conf)