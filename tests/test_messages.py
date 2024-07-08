from mockito import mock, when
import urllib3
from test_utils import sign_jwt_for_test, wrong_jwt_for_test, DATA_API_KEY, DATA_URL
import json
import datetime

import gateway


def test_get_all_chats_success_path():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn(
        [
            1234, 5678, 9012
        ])
    when(http).request("GET", f"http://{DATA_URL}/get_chats?userId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps([
            "1234", "5678", "9012"
        ])
    }
    actual = gateway.get_chats(http, token)
    assert expected == actual


def test_get_all_chats_invalid_token():
    http = mock(urllib3.PoolManager())

    token = wrong_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 401
    }
    actual = gateway.get_chats(http, token)
    assert expected == actual
    actual = gateway.get_chats(http, None)
    assert expected == actual


def test_get_chats_for_new_user_returns_empty_list():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"http://{DATA_URL}/get_chats?userId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps([])
    }
    actual = gateway.get_chats(http, token)
    assert expected == actual


def test_get_messages_success_path():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn(
        [{
            "message_id": 1234,
            "sender_id": 5678,
            "message_content": "Hello, World!",
            "created_on": "2000-01-01T00:00:00+00:00"
        }
        ,{
            "message_id": 3456,
            "sender_id": 7890,
            "message_content": "Goodbye, World!",
            "created_on": "2100-01-01T00:00:00+00:00"
        }
        ])
    when(http).request("GET", f"http://{DATA_URL}/get_messages?chatId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps( {
            "messages": [
                {
                    "messageId": "1234",
                    "senderId": "5678",
                    "content": "Hello, World!",
                    "timestamp": "2000-01-01T00:00:00+00:00"
                },
                {
                    "messageId": "3456",
                    "senderId": "7890",
                    "content": "Goodbye, World!",
                    "timestamp": "2100-01-01T00:00:00+00:00"
                }
            ]
        }
                
        )
    }

    actual = gateway.get_messages(http, token, 1234)
    assert expected == actual

def test_get_messages_invalid_token():
        http = mock(urllib3.PoolManager())
        token = wrong_jwt_for_test({
            "uid": 1234
        })

        expected = {
            "statusCode": 401,
        }
        actual = gateway.get_messages(http, token, 5678)
        assert expected == actual


def test_get_messages_invalid_chatid():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"http://{DATA_URL}/get_messages?chatId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "chatId does not exist"
        })
    }
    actual = gateway.get_messages(http, token, 1234)
    assert expected == actual


def test_get_messages_invalid_token():
    http = mock(urllib3.PoolManager())

    token = wrong_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 401
    }
    actual = gateway.get_messages(http, token, 1234)
    assert expected == actual
    actual = gateway.get_messages(http, None, 1234)
    assert expected == actual


def test_get_chat_preview_success_path():
    http = mock(urllib3.PoolManager())

    first_response = mock({
        "status": 200,
    })
    when(first_response).json().thenReturn({
        "seller": 5678,
        "buyer": 9012,
        "listing_id": 3456
    })
    when(http).request("GET", f"http://{DATA_URL}/get_chat_info?chatId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(first_response)
    second_response = mock({
        "status": 200,
    })
    when(second_response).json().thenReturn({
        "timestamp": "2010-01-01T00:00:00+00:00",
    })
    when(http).request("GET", f"http://{DATA_URL}/get_last_message_timestamp?chatId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(second_response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps({
            "users": ["5678", "9012"],
            "listingId": "3456",
            "lastMessageTime": "2010-01-01T00:00:00+00:00"
        })
    }
    actual = gateway.get_chat_preview(http, token, 1234)
    assert expected == actual


def test_get_chat_preview_invalid_token():
    http = mock(urllib3.PoolManager())

    token = wrong_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 401
    }
    actual = gateway.get_chat_preview(http, token, 1234)
    assert expected == actual
    actual = gateway.get_chat_preview(http, None, 1234)
    assert expected == actual


def test_get_chat_preview_invalid_chatid():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"http://{DATA_URL}/get_chat_info?chatId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "chatId not found"
        })
    }
    actual = gateway.get_chat_preview(http, token, 1234)
    assert expected == actual


def test_write_new_message_success_path():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "seller": 3456,
        "buyer": 5678,
    })

    when(http).request("GET", f"http://{DATA_URL}/get_chat_info?chatId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    create_body = {
        "chatId": 1234,
        "content": "Hi there",
        "senderId": 5678,
    }
    when(http).request("POST", f"http://{DATA_URL}/create_message", json=create_body, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 200
    }
    actual = gateway.write_message(http, token, 1234, "Hi there")
    assert expected == actual


def test_write_new_message_invalid_creds():
    http = mock(urllib3.PoolManager())
    token = wrong_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 401
    }
    actual = gateway.write_message(http, token, 1234, "Hi there")
    assert expected == actual


def test_write_new_message_invalid_chat_id():
    http = mock(urllib3.PoolManager())
    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"http://{DATA_URL}/get_chat_info?chatId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "chatId not found"
        })
    }
    actual = gateway.write_message(http, token, 1234, "Hi there! :)")
    assert expected == actual


def test_write_new_message_invalid_sender_id():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "seller": 3456,
        "buyer": 7890,
    })

    when(http).request("GET", f"http://{DATA_URL}/get_chat_info?chatId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 401
    }
    actual = gateway.write_message(http, token, 1234, "Hi there")
    assert expected == actual
