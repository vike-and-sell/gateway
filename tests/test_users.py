from mockito import when, mock, verify
import urllib3
import json
from test_utils import DATA_URL, sign_jwt_for_test, DATA_API_KEY, MAPS_API_KEY
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
        "address": "V8W",
        # jan 1, 2000 12am GMT
        "joining_date": "2000-01-01T00:00:00+00:00",
    })
    when(http).request("GET", f"{DATA_URL}/get_user?userId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    sales_response = mock({
        "status": 200,
    })
    when(sales_response).json().thenReturn(
        [12345, 67890]
    )
    when(http).request("GET", f"{DATA_URL}/get_user_sales?userId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(sales_response)

    purchases_response = mock({
        "status": 200,
    })
    when(purchases_response).json().thenReturn(
        [56789, 98765]
    )
    when(http).request("GET", f"{DATA_URL}/get_user_purchases?userId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(purchases_response)

    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps({
            "userId": 5678,
            "username": "bob1",
            "location": "V8W",
            "joiningDate": "2000-01-01T00:00:00+00:00",
            "itemsSold": [12345, 67890],
            "itemsPurchased": [56789, 98765],
        })
    }
    actual = gateway.get_user_by_id(http, token, 5678)
    assert expected == actual


def test_get_user_by_id_does_not_exist():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"{DATA_URL}/get_user?userId=5678", json=None, headers={
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
    address = "500 Fort St, Victoria, BC V8W 1E5"

    http = mock(urllib3.PoolManager())

    geocode_response = mock({
        "status": 200,
    })
    when(geocode_response).json().thenReturn({
        "results": [
            {
                "position": {
                    "lat": 123,
                    "lon": 456,
                },
                "address": {
                    "postalCode": "V8W"
                }
            }
        ]
    })
    when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                       .format(MAPS_API_KEY, address)).thenReturn(geocode_response)

    response = mock({
        "status": 200,
    })
    when(http).request("POST", f"{DATA_URL}/update_user", json={
        "userId": 5678,
        "address": "V8W",
        "location": {
            "lat": 123,
            "lng": 456
        }
    }, headers={
        "X-Api-Key": DATA_API_KEY
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 200,
    }
    actual = gateway.update_user(
        http, token, "500 Fort St, Victoria, BC V8W 1E5")
    assert expected == actual


def test_update_user_by_id_invalid_creds():
    http = mock(urllib3.PoolManager())

    expected = {
        "statusCode": 401,
    }
    actual = gateway.update_user(
        http, None, "500 Fort St, Victoria, BC V8W 1E5")
    assert expected == actual
    actual = gateway.update_user(http, sign_jwt_for_test(
        {}), "500 Fort St, Victoria, BC V8W 1E5")
    assert expected == actual


def test_update_user_by_id_invalid_address():
    http = mock(urllib3.PoolManager())
    address = "unparsable"

    geocode_response = mock({
        "status": 200,
    })
    when(geocode_response).json().thenReturn({
        "results": []
    })
    when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                       .format(MAPS_API_KEY, address)).thenReturn(geocode_response)

    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid address"
        })
    }
    actual = gateway.update_user(
        http, token, address)
    assert expected == actual


def test_get_user_by_me_success_path():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "username": "bob1",
        "location": "12.3456,78.9012",
        "address": "V8W",
        # jan 1, 2000 12am GMT
        "joining_date": "2000-01-01T00:00:00+00:00",
        "items_sold": [12345, 67890],
        "items_purchased": [56789, 98765],
        "charity": False
    })
    when(http).request("GET", f"{DATA_URL}/get_user?userId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    sales_response = mock({
        "status": 200,
    })
    when(sales_response).json().thenReturn(
        [12345, 67890]
    )
    when(http).request("GET", f"{DATA_URL}/get_user_sales?userId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(sales_response)

    purchases_response = mock({
        "status": 200,
    })
    when(purchases_response).json().thenReturn(
        [56789, 98765]
    )
    when(http).request("GET", f"{DATA_URL}/get_user_purchases?userId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(purchases_response)

    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps({
            "userId": 5678,
            "username": "bob1",
            "location": "V8W",
            "joiningDate": "2000-01-01T00:00:00+00:00",
            "itemsSold": [12345, 67890],
            "itemsPurchased": [56789, 98765],
            "seeCharity": False
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
    when(response).json().thenReturn([
        {'search_date': '2024-01-01T00:00:00', 'search_text': "bike"},
        {'search_date': '2024-01-01T00:00:00', 'search_text': "car"},
        {'search_date': '2024-01-01T00:00:00', 'search_text': "textbook"}
    ])
    when(http).request("GET", f"{DATA_URL}/get_search_history?userId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 200,
        "body": json.dumps(["bike", "car", "textbook"])
    }
    actual = gateway.get_search_history(http, token)
    assert expected == actual


def test_get_user_by_me_invalid_creds():
    http = mock(urllib3.PoolManager())

    expected = {
        "statusCode": 401,
    }

    actual = gateway.get_search_history(http, None)
    assert expected == actual

    actual = gateway.get_search_history(
        http, sign_jwt_for_test({}))
    assert expected == actual
