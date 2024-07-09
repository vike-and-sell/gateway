from mockito import when, mock, verify
import urllib3
import json
from test_utils import sign_jwt_for_test, DATA_API_KEY, MAPS_API_KEY
import datetime
from freezegun import freeze_time

import gateway


def test_request_account():
    email = "test@uvic.ca"
    callback = "http://callback"
    response = mock({
        "status": 200,
    })

    when(response).json().thenReturn()
    expected = {"statusCode": 200}
    actual = gateway.request_account(email, callback)
    assert actual == expected


def test_verify_account():
    with freeze_time("2024-06-29T17:45:28"):
        http = mock(urllib3.PoolManager())
        token = sign_jwt_for_test({
            "eml": "test@uvic.ca",
        })
        username = "test_user"
        password = "Test_password1"
        address = "500 Fort St, Victoria, BC V8W 1E5"
        response = mock({
            "status": 200,
        })

        geocode_response = mock({
            "status": 200,
        })
        when(geocode_response).json().thenReturn({
            "results": [
                {
                    "position": {
                        "lat": 123,
                        "lon": 456,
                    }
                }
            ]
        })

        when(response).json().thenReturn({
            "user_id": 1234
        })

        when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                           .format(MAPS_API_KEY, address)).thenReturn(geocode_response)

        when(http).request("POST", "http://test/make_user", json={
            "email": "test@uvic.ca",
            "username": username,
            "password": "02f51e9851b626f8a400c90d297141fecc50aa4b105f72b097126fd9949fa9ce",
            "address": address,
            "location": {"lat": 123, "lng": 456},
            "join_date": datetime.datetime.now(datetime.UTC).isoformat()
        }, headers={
            "X-Api-Key": DATA_API_KEY
        }).thenReturn(response)

        when(http).request("POST", "http://test/verify_account", body={
            "jwt": token,
            "username": username,
            "password": password,
            "address": address
        }, headers={
            "X-Api-Key": DATA_API_KEY,
        }).thenReturn(response)

        exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=3)
        expected = {
            "statusCode": 201,
            "body": json.dumps({
                "userId": 1234
            }),
            "auth": {
                "exp": exp,
                "jwt": sign_jwt_for_test({
                    "exp": exp,
                    "uid": 1234
                })
            }
        }

        actual = gateway.verify_account(
            http, token, username, password, address)
        assert expected == actual


def test_verify_account_invalid_username():
    http = mock(urllib3.PoolManager())
    token = sign_jwt_for_test({
        "eml": "test@uvic.ca",
    })
    username = "#"
    password = "Test_password1"
    address = "500 Fort St, Victoria, BC V8W 1E5"
    response = mock({
        "statusCode": 400,
        "body": json.dumps({
            "message": "Username does not meet the requirements"
        })
    })

    when(response).json().thenReturn({
        "user_id": 1234
    })

    when(http).request("POST", "http://test/verify_account", body={
        "jwt": token,
        "username": username,
        "password": password,
        "address": address
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Username does not meet the requirements"
        })
    }

    actual = gateway.verify_account(http, token, username, password, address)
    assert expected == actual


def test_verify_account_invalid_email():
    http = mock(urllib3.PoolManager())
    token = sign_jwt_for_test({
        "eml": "test",
    })
    username = "test_user"
    password = "Test_password1"
    address = "500 Fort St, Victoria, BC V8W 1E5"
    response = mock({
        "statusCode": 400,
        "body": json.dumps({
            "message": "Email does not meet the requirements"
        })
    })

    when(response).json().thenReturn({
        "user_id": 1234
    })

    when(http).request("POST", "http://test/verify_account", body={
        "jwt": token,
        "username": username,
        "password": password,
        "address": address
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Email does not meet the requirements"
        })
    }

    actual = gateway.verify_account(http, token, username, password, address)
    assert expected == actual


def test_verify_account_invalid_password():
    http = mock(urllib3.PoolManager())
    token = sign_jwt_for_test({
        "eml": "test@uvic.ca",
    })
    username = "test_user"
    password = "Test"
    address = "500 Fort St, Victoria, BC V8W 1E5"
    response = mock({
        "statusCode": 400,
        "body": json.dumps({
            "message": "Password does not meet the requirements"
        })
    })

    when(response).json().thenReturn({
        "user_id": 1234
    })

    when(http).request("POST", "http://test/verify_account", body={
        "jwt": token,
        "username": username,
        "password": password,
        "address": address
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Password does not meet the requirements"
        })
    }

    actual = gateway.verify_account(http, token, username, password, address)
    assert expected == actual


def test_login():
    with freeze_time("2024-06-29T17:45:28"):
        http = mock(urllib3.PoolManager())
        username = "john_doe"
        password = "Password123!"

        response = mock({
            "status": 200,
        })

        getinforesponse = mock({
            "status": 200,
            "body": {
                "user_id": 1234,
                "password": "Password123!"
            }
        })

        when(response).json().thenReturn()

        when(getinforesponse).json().thenReturn({
            "user_id": 1234,
            "password": "8b053b0b4813dc1986827113c07d5edc9a206f12244e9432cb0a98419a15ab66"
        })

        when(http).request("GET", "http://test/get_user_info_for_login?usr=john_doe", json=None,
                           headers={
                               "X-Api-Key": DATA_API_KEY,
                           }).thenReturn(getinforesponse)

        when(http).request("POST", "http://test/login", body={
            "username": username,
            "password": password
        }, headers={
            "X-Api-Key": DATA_API_KEY,
        }).thenReturn(response)

        exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=3)
        expected = {
            "statusCode": 200,
            "auth": {
                "exp": exp,
                "jwt": sign_jwt_for_test({
                    "exp": int(exp.timestamp()),
                    "uid": 1234,
                })
            }
        }

        actual = gateway.login(http, username, password)
        assert actual == expected


def test_login_user_not_exists():
    http = mock(urllib3.PoolManager())
    username = "test_user"
    password = "Test_pass1"

    response = mock({
        "statusCode": 400,
        "body": json.dumps({
            "message": ""
        })
    })

    when(response).json().thenReturn()

    when(http).request("GET", "http://test/get_user_info_for_login?usr=test_user", json=None,
                       headers={
                           "X-Api-Key": DATA_API_KEY,
                       }).thenReturn(response)

    when(http).request("POST", "http://test/login", body={
        "username": username,
        "password": password
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": ""
        })
    }

    actual = gateway.login(http, username, password)
    assert actual == expected


def test_login_incorrect_password():
    http = mock(urllib3.PoolManager())
    username = "john_doe"
    password = "Test_pass1"

    response = mock({
        "statusCode": 400,
        "body": json.dumps({
            "message": ""
        })
    })

    when(response).json().thenReturn()

    when(http).request("GET", "http://test/get_user_info_for_login?usr=john_doe", json=None,
                       headers={
                           "X-Api-Key": DATA_API_KEY,
                       }).thenReturn(response)

    when(http).request("POST", "http://test/login", body={
        "username": username,
        "password": password
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": ""
        })
    }

    actual = gateway.login(http, username, password)
    assert actual == expected


def test_request_reset():
    email = "test@uvic.ca"
    callback = "http://callback"

    response = mock({
        "status": 200,
    })

    when(response).json().thenReturn()
    expected = {"statusCode": 200}
    actual = gateway.request_account(email, callback)
    assert actual == expected


def test_request_reset_invalid_email():
    email = "test"
    callback = "http://callback"

    response = mock({
        "status": 400,
        "body": json.dumps({
            "message": ""
        })
    })

    when(response).json().thenReturn()
    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": ""
        })
    }
    actual = gateway.request_account(email, callback)
    assert actual == expected


def test_verify_reset():
    http = mock(urllib3.PoolManager())
    token = sign_jwt_for_test({
        "eml": "john_doe@uvic.ca",
    })
    password = "Test_password1"

    response = mock({
        "status": 200,
    })
    emlresponse = mock({
        "status": 200,
        "body": json.dumps({
            "user_id": 1234,
            "username": "john_doe"
        })
    })

    when(response).json().thenReturn()
    when(emlresponse).json().thenReturn({
        "user_id": 1234,
        "username": "john_doe"
    })
    when(http).request("GET", "http://test/get_user_by_email?eml=john_doe@uvic.ca", json=None,
                       headers={
                           "X-Api-Key": DATA_API_KEY,
                       }).thenReturn(emlresponse)

    when(http).request("POST", "http://test/update_user_password", json={
        "user_id": 1234,
        "password": "ade53186e7d85ebd0e7d45eed46e9b663090be24147663496434041329b40916"
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    when(http).request("POST", "http://test/verify_reset", body={
        "token": token,
        "password": password
    }).thenReturn(response)

    expected = {
        "statusCode": 200,
    }

    actual = gateway.verify_reset(http, token, password)
    assert actual == expected


def test_verify_reset_invalid_email():
    http = mock(urllib3.PoolManager())
    token = sign_jwt_for_test({
        "eml": "test",
    })
    password = "Test_password1"

    response = mock({
        "status": 500,
    })
    emlresponse = mock({
        "status": 500,
    })

    when(response).json().thenReturn()
    when(emlresponse).json().thenReturn({
        "user_id": 1234,
        "username": "john_doe"
    })
    when(http).request("GET", "http://test/get_user_by_email?eml=test", json=None,
                       headers={
                           "X-Api-Key": DATA_API_KEY,
                       }).thenReturn(emlresponse)

    when(http).request("POST", "http://test/update_user_password", json={
        "user_id": 1234,
        "password": "ade53186e7d85ebd0e7d45eed46e9b663090be24147663496434041329b40916"
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    when(http).request("POST", "http://test/verify_reset", body={
        "token": token,
        "password": password
    }).thenReturn(response)

    expected = {
        "statusCode": 500,
    }

    actual = gateway.verify_reset(http, token, password)
    assert actual == expected
