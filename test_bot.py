from app import Application
from http import HTTPStatus
import json
import pytest
import tornado
from tornado.httpclient import HTTPClientError
import unittest
import read_config
import os
import http.client
import json
import ssl
import errors_code

addr = '127.0.0.1'
port = int(os.environ.get('PORT', 5000))


@pytest.fixture
def app():
    application = Application(debug=False)
    return application


async def test_spec_start_1(http_server_client):
    """
    Ввели команду старт и не поздаровались.
    """
    req = {'update_id': 588992740, 'message': {'message_id': 2011,
                                               'from': {'id': 322608291, 'is_bot': False, 'first_name': 'Алексей',
                                                        'last_name': 'Простаков', 'username': 'prostakov_alexey',
                                                        'language_code': 'ru'},
                                               'chat': {'id': 322608291, 'first_name': 'Алексей',
                                                        'last_name': 'Простаков', 'username': 'prostakov_alexey',
                                                        'type': 'private'}, 'date': 1566312765, 'text': '/help',
                                               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}
    patch_response = await http_server_client.fetch('/bot', method='POST', body=json.dumps(req))
    if patch_response.code == HTTPStatus.OK:
        req = {'update_id': 588992740, 'message': {'message_id': 2011,
                                                   'from': {'id': 322608291, 'is_bot': False, 'first_name': 'Алексей',
                                                            'last_name': 'Простаков', 'username': 'prostakov_alexey',
                                                            'language_code': 'ru'},
                                                   'chat': {'id': 322608291, 'first_name': 'Алексей',
                                                            'last_name': 'Простаков', 'username': 'prostakov_alexey',
                                                            'type': 'private'}, 'date': 1566312765, 'text': '/start',
                                                   'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}
        patch_response = await http_server_client.fetch('/bot', method='POST', body=json.dumps(req))
        assert patch_response.code == HTTPStatus.OK
        resp = json.loads(patch_response.body, encoding='utf-8')
        assert resp['text'] == errors_code.get_error(4, 'ru')


async def test_spec_start_2(http_server_client):
    """
    Неправильный формат команды /start 1000 - команды со слишком большим номером
    """
    req = {'update_id': 588992740, 'message': {'message_id': 2011,
                                               'from': {'id': 322608291, 'is_bot': False, 'first_name': 'Алексей',
                                                        'last_name': 'Простаков', 'username': 'prostakov_alexey',
                                                        'language_code': 'ru'},
                                               'chat': {'id': 322608291, 'first_name': 'Алексей',
                                                        'last_name': 'Простаков', 'username': 'prostakov_alexey',
                                                        'type': 'private'}, 'date': 1566312765, 'text': '/start 1000',
                                               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}
    patch_response = await http_server_client.fetch('/bot', method='POST', body=json.dumps(req))
    assert patch_response.code == HTTPStatus.OK
    resp = json.loads(patch_response.body, encoding='utf-8')
    assert resp['text'] == errors_code.get_error(2, 'ru')
