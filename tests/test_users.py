from mockito import when, mock, verify
import urllib3
import json
from test_utils import sign_jwt_for_test, DATA_API_KEY
import datetime

import gateway


def test_get_user_by_id_success_path():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "username": "bob1",
        "email": "bob1@uvic.ca",
        "location": "12.3456,78.9012",
        "address": "500 Fort St, Victoria, BC V8W 1E5",
        # jan 1, 2000 12am GMT
        "joining_date": datetime.datetime.fromisoformat("2000-01-01T00:00:00Z"),
        "items_sold": [12345, 67890],
        "items_purchased": [56789, 98765],
    })
    when(http).request("GET", "http://test/get_user?userId=5678", body=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps({
            "username": "bob1",
            "location": "V8W",
            "joiningDate": "2000-01-01T00:00:00+00:00",
            "itemsSold": ["12345", "67890"],
            "itemsPurchased": ["56789", "98765"],
        })
    }
    actual = gateway.get_user_by_id(http, token, 5678)
    assert expected == actual


def test_get_user_by_id_does_not_exist():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 404,
    })
    when(http).request("GET", "http://test/get_user?userId=5678", body=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "User not found",
        }),
    }
    actual = gateway.get_user_by_id(http, token, 5678)
    assert expected == actual


def test_get_user_by_id_no_creds():
    http = mock(urllib3.PoolManager())
    expected = {
        "statusCode": 401,
    }
    actual = gateway.get_user_by_id(http, None, 5678)
    assert expected == actual

    actual = gateway.get_user_by_id(http, sign_jwt_for_test({}), 5678)
    assert expected == actual


def test_update_user_by_id_success_path():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(http).request("POST", "http://test/update_user", body={
        "userId": 5678,
        "address": "500 Fort St, Victoria, BC V8W 1E5"
    }, headers={
        "X-Api-Key": DATA_API_KEY
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 200,
    }
    actual = gateway.update_user_by_id(
        http, token, 5678, "500 Fort St, Victoria, BC V8W 1E5")
    assert expected == actual


def test_update_user_by_id_wrong_token_uid():
    http = mock(urllib3.PoolManager())
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 401,
    }
    actual = gateway.update_user_by_id(
        http, token, 1234, "500 Fort St, Victoria, BC V8W 1E5")

    assert expected == actual


def test_update_user_by_id_invalid_creds():
    http = mock(urllib3.PoolManager())

    expected = {
        "statusCode": 401,
    }
    actual = gateway.update_user_by_id(
        http, None, 5678, "500 Fort St, Victoria, BC V8W 1E5")
    assert expected == actual
    actual = gateway.update_user_by_id(http, sign_jwt_for_test(
        {}), 5678, "500 Fort St, Victoria, BC V8W 1E5")
    assert expected == actual


def test_update_user_by_id_invalid_address():
    http = mock(urllib3.PoolManager())

    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid address"
        })
    }
    actual = gateway.update_user_by_id(
        http, token, 5678, "unparsable_address")
    assert expected == actual


def test_get_user_by_me_success_path():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "username": "bob1",
        "email": "bob1@uvic.ca",
        "location": "12.3456,78.9012",
        "address": "500 Fort St, Victoria, BC V8W 1E5",
        # jan 1, 2000 12am GMT
        "joining_date": datetime.datetime.fromisoformat("2000-01-01T00:00:00Z"),
        "items_sold": [12345, 67890],
        "items_purchased": [56789, 98765],
    })
    when(http).request("GET", "http://test/get_user?userId=5678", body=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps({
            "username": "bob1",
            "location": "V8W",
            "joiningDate": "2000-01-01T00:00:00+00:00",
            "itemsSold": ["12345", "67890"],
            "itemsPurchased": ["56789", "98765"],
        })
    }
    actual = gateway.get_user_by_auth_token(http, token)
    assert expected == actual


def test_get_user_by_me_invalid_creds():
    http = mock(urllib3.PoolManager())

    expected = {
        "statusCode": 401,
    }

    actual = gateway.get_user_by_auth_token(http, None)
    assert expected == actual

    actual = gateway.get_user_by_auth_token(http, sign_jwt_for_test({}))
    assert expected == actual


def test_get_user_search_history_success_path():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "searches": ["bike", "car", "textbook"]
    })
    when(http).request("GET", "http://test/get_searches?userId=5678", body=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps(["bike", "car", "textbook"])
    }
    actual = gateway.get_search_history_by_id(http, token, 5678)
    assert expected == actual


def test_get_user_by_me_invalid_creds():
    http = mock(urllib3.PoolManager())

    expected = {
        "statusCode": 401,
    }

    actual = gateway.get_search_history_by_id(http, None, 1234)
    assert expected == actual

    actual = gateway.get_search_history_by_id(
        http, sign_jwt_for_test({}), 1234)
    assert expected == actual
