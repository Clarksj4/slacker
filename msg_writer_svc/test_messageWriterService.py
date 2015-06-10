__author__ = 'clarksj4 & camertp1'

import requests
import json
from unittest import TestCase


class TestMessageWriterService(TestCase):
    heads = {'Content-Type': 'application/json'}

    def test_POST_type_error(self):
        """ Tests appropriate error message is returned when the passed variable is not json
        """
        invalid_type = 72
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(invalid_type))
        self.assertEquals(response.json(),
                          {"new_msg_response": {
                              "response_message": "Invalid POST request: post data did not contain valid json",
                              "response_code": 31}})

    def test_POST_format_error(self):
        """ Tests appropriate error msg is returned when json has invalid format
        """
        invalid_format = {'blargh': 'baz'}
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(invalid_format))
        self.assertEquals(response.json(),
                          {"new_msg_response": {
                              "response_message": "Invalid POST request: post data was missing parameter(s)",
                              "response_code": 32}})

    def test_POST_invalid_session(self):
        """ Tests appropriate error is returned when an invalid session key is used
        """
        invalid_session_key = {"message": {"channel_id": 0, "session_key": 'zzzzzzzzz', "body": "message"}}
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(invalid_session_key))
        self.assertEquals(response.json(),
                          {"new_msg_response": {
                              "response_message": "Invalid session key: authorisation failed",
                              "response_code": 33}})

    def test_POST_invalid_channel(self):
        """ Tests appropriate error is returned when an invalid channel is used
        """
        invalid_channel_id = {"message": {"channel_id": 'zzzzzzzzzz', "session_key": '0', "body": "message"}}
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(invalid_channel_id))
        self.assertEquals(response.json(),
                          {"new_msg_response": {
                              "response_message": "Channel invalid",
                              "response_code": 1}})

    def test_POST_success_message(self):
        """ Tests appropriate success message is returned when a valid message is posted
        """
        valid_message = {"message": {"channel_id": '1', "session_key": '1', "body": "message"}}
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(valid_message))
        self.assertEquals(response.json(),
                          {"new_msg_response": {
                              "response_message": "Message entered successfully",
                              "response_code": 0,
                              "message_id": 1}})