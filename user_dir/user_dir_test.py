import unittest
import requests
import json
import sys
lib_path = '..'
sys.path.append(lib_path)
import slacker_config

# Author: Matt Ankerson
# Date: 28 May 2015


class UserDirTest(unittest.TestCase):
    
    def setUp(self):
        self.service_url = slacker_config.urls.url['user_directory'] + ":" + str(slacker_config.urls.port['user_directory'])
        self.heads = {'Content-Type': 'application/json'}
        self.good_user = {'email': 'yogi@bear', 'password': 'yellowstone', 'screen_name': 'picnic_baskets'}
        self.good_user1 = {'email': 'yogi@bear1', 'password': 'yellowstone', 'screen_name': 'picnic_baskets'}
        self.addition_success = {'response': 'success'}
        
        self.existing_user = {'email': 'yogi@bear', 'password': 'yellowstone'}
        self.unique_user = {'email': 'snoop@dogg', 'password': 'ginandjuice'}
        self.existing_user_false_password = {'email': 'yogi@bear', 'password': 'yeahnah'}
        self.response_existing = {'email': 'unavailable', 'password': 'correct'}
        self.response_unique = {'email': 'available', 'password': 'not set'}
        self.response_user_false_password = {'email': 'unavailable', 'password': 'incorrect'}
        
    def test_post(self):
        good_user_result = requests.post(self.service_url, data=json.dumps(self.good_user), headers=self.heads).json()
        self.assertDictEqual(good_user_result, self.addition_success)
        
    def test_get(self):
        existing_user = requests.get(self.service_url, params=self.existing_user).json()
        new_user = requests.get(self.service_url, params=self.unique_user).json()
        false_password = requests.get(self.service_url, params=self.existing_user_false_password).json()
        self.assertDictEqual(self.response_existing, existing_user)
        self.assertDictEqual(self.response_unique, new_user)
        self.assertDictEqual(self.response_user_false_password, false_password)
        
if __name__ == '__main__':
    unittest.main()