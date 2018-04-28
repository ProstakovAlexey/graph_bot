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


port = 8443
addr = '192.168.0.120'

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


class CaseConfig(unittest.TestCase):
    """This class testing function for read and verification configuration file"""
    def test1_good(self):
        """Read good config file, have not error"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_1.ini')
        self.assertFalse(error)

    def test2_err(self):
        """Config file have bad token files"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_2.ini')
        self.assertEqual(error, 'File with tokens is not found. ')

    def test3_err(self):
        """Config file have not description for dot file"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_3.ini')
        self.assertEqual(error, 'Graph description is empty. ')

    def test4_err(self):
        """Config file have bad dot files"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_4.ini')
        self.assertEqual(error, 'Graph file with name err/1.gv is not found. ')

    def test5_err(self):
        """Config file have not graph name"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_5.ini')
        self.assertEqual(error, 'Graph name is empty. ')


class CaseDot(unittest.TestCase):
    """This class testing function for graph algoritm"""
    def test1_way(self):
        """Load config and checking data"""
        error, graphs, tokens, log, lang = read_config.read_config('for_tests/config_6.ini')
        self.assertFalse(error)
        graph_object_list = list()
        for graph in graphs:
            gr = pydotplus.graphviz.graph_from_dot_file(graph['file_name'])
            graph_object_list.append(functions.parse_dot(gr))
        self.assertEqual(len(graph_object_list), 1)
        good = (
            {
                'node': 'node',
                'Start': 'Start',
                'T1': 'Node #1. Only one way.',
                'T2': 'Node #2, have question with choice. What choice you?',
                'T3a': 'Node #3a. You was say YES',
                'T3b': 'Node #3b. You was say NO',
                'T4': 'Finish node #4. One way.',
                'End': 'End'
            },
            [
                ['Start', 'T1', None],
                ['T1', 'T2', None],
                ['T2', 'T3a', 'YES'],
                ['T2', 'T3b', 'NO'],
                ['T3a', 'T4', None],
                ['T3b', 'T4', None],
                ['T4', 'End', None]
            ]
        )
        self.assertEqual(good[0], graph_object_list[0][0],
                         'Error in function for read graph file. Problem with node list.')
    """
    POST requests.Format:
    {
        'token':
        'user_id':
        'user_name':
        'text':
    }
    """
    def test2_service(self):
        """Ask /end it delete history, must return 1
        """
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/end'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 1)

    def test3_service(self):
        """Ask service. Before test run you need start service with config file config6 and port=8000.
        This is ask for new user, must return 6
        """
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': 'Hello!'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 6)

    def test4_service(self):
        """Ask /help, must return 4
        """
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/help'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 4)

    def test5_service(self):
        """Ask /list, must return 5
        """
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/list'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 5)

    def test6_service(self):
        """Ask /start it is bad format, must return 3
        """
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/start'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 3)

    def test7_service(self):
        """Ask /start 2 it is bad format, must return 3
        """
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/start 2'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 2)

    def test8_service(self):
        """
        Check edge with YES. /end, /start 1
        """
        # end
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/end'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 1)
        # start
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/start 1'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('Node #1') == -1:
            self.fail('Need return Node #1')
        # ok
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': ''
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('Node #2') == -1:
            self.fail('Need return Node #2')
        # Choice  YES, must return node #3a
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '1'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('Node #3a') == -1:
            self.fail('Need return Node #3a')

        # Ask any thinks, and  go to next node, must return node #4
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': ''
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('node #4') == -1:
            self.fail('Need return Node #4')

        # Ask any thinks, and  return node End, it is finish for graph
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': ''
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        self.assertEqual(resp['text'], 'End')

    def test9_service(self):
        """This is big test. We go to edge NO. Will go /end, /start 1, 'ok', choice NO(1), ok, ok and return end
        """
        # end
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/end'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 1)
        # start 1
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/start 1'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        # ok
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': 'ok'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        # choice NO
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '2'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('Node #3b') == -1:
            self.fail('Need return Node #3b, ask %s' % resp['text'])
        # ok
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': 'ok'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('node #4') == -1:
            self.fail('Need return Node #4')
        # end
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': 'ok'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        self.assertEqual(resp['text'], 'End')

    def test10_service(self):
        """If user ask /start 1 in middle graph, must go to first node"""
        # end
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/end'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 1)
        # start 1 - select graph 1
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/start 1'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('Node #1') == -1:
            self.fail('Need return Node #1, was return %s' % resp)
        # ok
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': 'ok'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('Node #2') == -1:
            self.fail('Need return Node #2')
        # start 1 - select graph 1
        req = {
            'token': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/start 1'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 0)
        if resp['text'].find('Node #1') == -1:
            self.fail('Need return Node #1')

    def test11_service(self):
        """Ask in bad format (tokens), must return 1
        """
        req = {
            'tokens': 'test_token',
            'user_id': '123-123',
            'user_name': 'Tester',
            'text': '/end'
        }
        resp = ask_bot(addr, port, req)
        self.assertEqual(resp['status'], 'ERROR')

