#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Tests for project dot_bot
"""

import unittest
import read_config
import functions
import pydotplus
import http.client
import json
import ssl


port = 8888
addr = '127.0.0.1'


def ask_bot(address, port, request):
    """
    Send request in service
    :param address: service address
    :param port: service port
    :param request: json.dump and send
    :return: json.load form response
    """
    # context=ssl._create_unverified_context() - for use untrusted certs
    con = http.client.HTTPSConnection(address, port, context=ssl._create_unverified_context())
    headers = {"Content-Type": "text/json; charset=utf-8"}
    con.request("POST", '/bot', json.dumps(request).encode('utf-8'), headers=headers)
    result = con.getresponse().read()
    con.close()
    # print(result)
    return json.loads(result.decode('utf-8'))







