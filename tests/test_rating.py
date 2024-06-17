import datetime
from mockito import when, mock, verify
import pytest
import urllib3
import json
from test_utils import sign_jwt_for_test, DATA_API_KEY

import gateway

def test_get_ratings_success():
    http = mock(urllib3.PoolManager())

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn([
        {
        "username": "bob1",
        "created_on": datetime.datetime.fromisoformat("2001-01-01T00:00:00Z"),
        "rating": 3
        },
        {
        "username": "bob2",
        "created_on": datetime.datetime.fromisoformat("2003-01-11T00:00:00Z"),
        "rating": 4
        },
    ])

    when(http).request("GET", "http://test/get_ratings?listingId=5678", body=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 1234
    })

    expected = {
        "statusCode": 200,
        "body":json.dumps([
            {
            "username": "bob1",
            "created_on": "2001-01-01T00:00:00Z",
            "rating": 3
            },
            {
            "username": "bob2",
            "created_on": "2003-01-11T00:00:00Z",
            "rating": 4
            },
        ])
    }
    actual = gateway.get_ratings_by_listing_id(http, token, 5678)
    assert expected == actual

def test_get_ratings_unauthorized():
    http = mock(urllib3.PoolManager())

    expected = {
        "statusCode": 401,
    }
    actual = gateway.get_ratings_by_listing_id(http, None, 5678)
    assert expected == actual

    actual = gateway.get_ratings_by_listing_id(http, sign_jwt_for_test({}), 5678)
    assert expected == actual