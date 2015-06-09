import unittest
import requests
import json
import sys
lib_path = '..'
sys.path.append(lib_path)
import slacker_config

# Author: Matt Ankerson
# Date: 22 May 2015


class SignUpTests(unittest.TestCase):

    def setUp(self):
        self.service_url = slacker_config.urls.url['signup'] + ":" + str(slacker_config.urls.port['signup'])
        self.heads = {'Content-Type': 'application/json'}

        self.good_user = {'email': 'yogi@bear', 'password': 'yellowstone', 'screen_name': 'picnic_baskets'}
        self.user_missing_email = {'email': '', 'password': 'yellowstone', 'screen_name': 'picnic_baskets'}
        self.user_missing_password = {'email': 'yogi@bear', 'password': '', 'screen_name': 'picnic_baskets'}
        self.user_missing_scrn_name = {'email': 'yogi@bear', 'password': 'yellowstone', 'screen_name': ''}

        self.response_valid = {u'email': u'valid', u'password': u'valid', u'screen_name': u'valid'}
        self.response_bad_email = {u'email': u'invalid', u'password': u'valid', u'screen_name': u'valid'}
        self.response_bad_password = {u'email': u'valid', u'password': u'invalid', u'screen_name': u'valid'}
        self.response_bad_scrn_name = {u'email': u'valid', u'password': u'valid', u'screen_name': u'invalid'}

        self.add_user_successful = {u'response': u'success'}

    def test_get(self):
        check_good_user = requests.get(self.service_url, params=self.good_user).json()
        check_bad_email = requests.get(self.service_url, params=self.user_missing_email).json()
        check_bad_password = requests.get(self.service_url, params=self.user_missing_password).json()
        check_bad_scrn_nme = requests.get(self.service_url, params=self.user_missing_scrn_name).json()
        self.assertDictEqual(self.response_valid, check_good_user)
        self.assertDictEqual(self.response_bad_email, check_bad_email)
        self.assertDictEqual(self.response_bad_password, check_bad_password)
        self.assertDictEqual(self.response_bad_scrn_name, check_bad_scrn_nme)

    def test_post(self):
        #good_user = requests.post(self.service_url, data=json.dumps(self.good_user), headers=self.heads).json()
        good_user = requests.post(self.service_url, data=json.dumps(self.good_user), headers=self.heads).json()
        self.assertDictEqual(good_user, self.add_user_successful)

if __name__ == '__main__':
    unittest.main()