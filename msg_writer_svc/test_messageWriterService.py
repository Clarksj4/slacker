__author__ = 'clarksj4 & camertp1'

import requests
import json
from unittest import TestCase


class TestMessageWriterService(TestCase):
    heads = {'Content-Type': 'application/json'}

    def test_POST(self):
        # test appropriate error msg is returned when json has invalid format
        invalid_format = {'blargh': 'baz'}
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(invalid_format))
        self.assertEquals(response.json(),
                          {"new_msg_response": {"response_message": "Invalid POST request format: parameter missing",
                                                "response_code": 32}})

        # test appropriate error is returned when an invalid session key is used
        invalid_session_key = {"message": {"channel_id": 0, "session_key": 'zzzzzzzzz', "body": "message"}}
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(invalid_session_key))
        self.assertEquals(response.json(),
                          {"new_msg_response": {"response_message": "Invalid session key: authorisation failed",
                                                "response_code": 33}})

        # test appropriate error is returned when an invalid channel is used
        invalid_channel_id = {"message": {"channel_id": 'zzzzzzzzzz', "session_key": '0', "body": "message"}}
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(invalid_channel_id))
        self.assertEquals(response.json(),
                          {"new_msg_response": {"response_message": "Channel invalid",
                                                "response_code": 1}})

        # test appropriate success message is returned when an appropriate message is used
        valid_message = {"message": {"channel_id": '1', "session_key": '1', "body": "message"}}
        response = requests.post('http://localhost:8006/',
                                 headers=TestMessageWriterService.heads,
                                 data=json.dumps(valid_message))
        self.assertEquals(response.json(),
                          {"new_msg_response": {"response_message": "Message entered successfully",
                                                "response_code": 0,
                                                "message_id": 1}})

    def test__authorize(self):
        self.fail()

    def test__write(self):
        self.fail()