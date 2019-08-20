from app import Application
from http import HTTPStatus
import json
import pytest
import tornado
from tornado.httpclient import HTTPClientError


@pytest.fixture
def app():
    application = Application(debug=False)
    return application


async def test_auth_1(http_server_client):
    """
    Send request with good token
    """
    request = {"token": "test_token", "user_id": "122", "user_name": "name", "text": "hello"}
    patch_response = await http_server_client.fetch('/bot', method='POST', body=json.dumps(request))
    assert patch_response.code == HTTPStatus.OK


async def test_auth_2(http_server_client):
    """
    Send request with bad token
    """
    request = {"token": "test_tkn",  "user_id": "122", "user_name": "name", "text": "hello"}
    try:
        patch_response = await http_server_client.fetch('/bot', method='POST', body=json.dumps(request))
    except tornado.httpclient.HTTPClientError as err:
        assert err.message == 'Unauthorized'


async def test_auth_3(http_server_client):
    """
    Send request without token
    """
    request = {"user_id": "122", "user_name": "name", "text": "hello"}
    try:
        patch_response = await http_server_client.fetch('/bot', method='POST', body=json.dumps(request))
    except tornado.httpclient.HTTPClientError as err:
        assert err.message == 'Bad Request'
