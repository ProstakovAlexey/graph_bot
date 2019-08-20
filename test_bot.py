from app import Application
from http import HTTPStatus
import json
import pytest
import tornado
from tornado.httpclient import HTTPClientError
import unittest
import read_config


import http.client
import json
import ssl


addr = '127.0.0.1'
port = 8888

@pytest.fixture
def app():
    application = Application(debug=False)
    return application


async def test_spec_end(http_server_client):
    """
    Special command /end
    """
    req = {
        'token': 'test_token',
        'user_id': '123-123',
        'user_name': 'Tester',
        'text': '/end'
    }
    patch_response = await http_server_client.fetch('/bot', method='POST', body=json.dumps(req))
    assert patch_response.code == HTTPStatus.OK
    """
    body = patch_response.body.decode('utf-8')
    print('000', body)
    resp = json.loads(body)
    print('111', resp)
    assert resp['status'] == 1
    """

'''
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
'''