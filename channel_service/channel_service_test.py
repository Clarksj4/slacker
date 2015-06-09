__author__ = 'alexmcneill'

import unittest
import requests
import json

class ChannelServiceTests(unittest.TestCase):

    def setUp(self):
        self.service_url = "http://127.0.0.1:8003/"
        self.heads = {'Content-Type' : 'application/json'}

        #Variable's for testing the get channel
        self.valid_channel_id = 1
        self.existing_channel_response = {"channel_read_response": {"response_message": 'Channel found', "response_code": 0}}

        self.invalid_channel_id = -1
        self.no_channel_response = {}

        self.valid_new_channel_json = {"name": "Alex's test", "owner": 1}
        self.valid_new_channel_response = {}

        self.invalid_new_channel_json = {"nme": "Lex"}
        self.invalid_new_channel_response = {}


    def test_get_channel(self):
        get_channel_response = requests.get('http://localhost:8003/?channel_id=' + str(self.valid_channel_id)).json()
        self.assertDictEqual(self.existing_channel_response, get_channel_response)

        get_channel_response = requests.get('http://localhost:8003/?channel_id=' + str(self.invalid_channel_id)).json()
        self.assertDictEqual(self.no_channel_response, get_channel_response)

    def test_add_channel(self):
        add_channel_response = requests.post('http://localhost:8003/', headers=self.heads,
                      data=json.dumps(self.valid_new_channel_json))