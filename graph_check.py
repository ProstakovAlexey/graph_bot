#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Check graph in terminal mode
"""

import http.client
import json
import ssl
import uuid

port = 443
addr = 'polar-coast-24118.herokuapp.com'
token = 'test_token'
print('This program use for check graph files, loading in bot.')
input('Will be use address {0}, port {1}. Press ENTER for continue.'.format(addr, port))
name = input('What is you name?')
user_id = uuid.uuid1().hex
con = http.client.HTTPSConnection(addr, port, context=ssl._create_unverified_context())
headers = {"Content-Type": "text/json; charset=utf-8"}
ask = 'Hello!'
print('You can write exit for program close.')
while ask != 'exit':
    reply = {
            'token': token,
            'user_id': user_id,
            'user_name': name,
            'text': ask
        }
    #print(reply)
    con.request("POST", '/bot', json.dumps(reply).encode('utf-8'), headers=headers)
    result = con.getresponse().read()
    print(result)
    result = json.loads(result.decode('utf-8'))
    if 'error' in result:
        print('Bot response with errror. Error={0}, errorMessage={1}'.
              format(result['error'], result['errorMessage']))
        break
    print('Bot response with status={0} and text={1}'.format(result['status'], result['text']))
    ask = input('What is you reply?')
con.close()
