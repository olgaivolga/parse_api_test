#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: set ts=4 sts=4 sw=4 et:

import json
import httplib
import unittest
from datetime import datetime
import re

'''
Example test for parse.com API.
No negative testing
'''

def validate_date(d):
    try:
        datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%fZ') 
        return True
    except ValueError:
        return False

class TestFunction(unittest.TestCase):

    parseId = "aBVFDLZ1bywHY65yQtsAv57Qbgr3O2xZBnHzt8SJ"
    parseKey = "2wrecY9xNFu00RdPIDMRB0agtg6947zOOGFi6DCl"
    
    @classmethod
    def setUpClass(self):
        '''
        Post an item and save result to check in post() 
        Also save objectId to use in subsequent calls
        '''
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/classes/GameScore', json.dumps({
               "score": 1337,
               "playerName": "Sean Plott",
               "cheatMode": False
             }), {
               "X-Parse-Application-Id": self.parseId,
               "X-Parse-REST-API-Key": self.parseKey,
               "Content-Type": "application/json"
             })
        result = json.loads(connection.getresponse().read())
        self.post_result = result
        self.obj = result['objectId'] 

    @classmethod
    def tearDownClass(self):
        '''
        Delete the item after all tests. 
        But how do we test DELETE?
        '''
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('DELETE', '/1/classes/GameScore/'+TestFunction.obj, '', {
               "X-Parse-Application-Id": self.parseId,
               "X-Parse-REST-API-Key": self.parseKey
             })
        result = json.loads(connection.getresponse().read())

    def test_parse_api(self):
        '''
        A sort of wrapper to preserve execution order
        Bad practice really.
        '''
        self.post()
        self.get()
        self.put()
        self.updated()


    def post(self):
        print "Testing POST..."
        objectId_got = self.post_result['objectId']
        createdAt_got = self.post_result['createdAt']
        self.assertTrue(re.match(r'^(\w){10}$', objectId_got))
        self.assertTrue(validate_date(createdAt_got))


    def get(self):
        print "Testing GET..."
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('GET', '/1/classes/GameScore/'+TestFunction.obj, '', {
               "X-Parse-Application-Id": self.parseId,
               "X-Parse-REST-API-Key": self.parseKey 
             })
        result = json.loads(connection.getresponse().read())
        self.assertEqual(TestFunction.obj, result['objectId'])
        self.assertEqual('Sean Plott', result['playerName'])
        self.assertFalse(result['cheatMode'])
        self.assertEqual(1337, result['score'])
        self.assertEqual(result['createdAt'], result['updatedAt'])


    def put(self):
        print "Testing PUT..."
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('PUT', '/1/classes/GameScore/'+TestFunction.obj, json.dumps({
               "score": 73453
             }), {
               "X-Parse-Application-Id": self.parseId,
               "X-Parse-REST-API-Key": self.parseKey,
               "Content-Type": "application/json"
             })
        result = json.loads(connection.getresponse().read())
        updatedAt_got = result['updatedAt']
        self.assertTrue(validate_date(updatedAt_got))

    def updated(self):
        print "Testing updated item..."
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('GET', '/1/classes/GameScore/'+TestFunction.obj, '', {
               "X-Parse-Application-Id": self.parseId,
               "X-Parse-REST-API-Key": self.parseKey
             })
        result = json.loads(connection.getresponse().read())
        self.assertEqual(73453, result['score'])
        self.assertNotEqual(result['createdAt'], result['updatedAt'])


if __name__ == '__main__':
    unittest.main()
