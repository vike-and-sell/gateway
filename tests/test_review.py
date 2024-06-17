import datetime
from mockito import when, mock, verify
import pytest
import urllib3
import json
from test_utils import sign_jwt_for_test, DATA_API_KEY

import gateway

@pytest.fixture(scope='module', autouse=True)
def setup_module():
    http = mock(urllib3.PoolManager())
    token = sign_jwt_for_test({
        "uid": 1234
    })
    return http, token

def test_get_reviews_success(setup_module):
    http, token = setup_module

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn([
        {
        "username": "bob1",
        "created_on": datetime.datetime.fromisoformat("2001-01-01T00:00:00Z"),
        "review": "holy wow! this newfangled gizmo is so rad!"
        },
        {
        "username": "bob2",
        "created_on": datetime.datetime.fromisoformat("2003-01-11T00:00:00Z"),
        "review": "... this item totally sucks :("
        },
    ])

    when(http).request("GET", "http://test/get_reviews?listingId=5678", body=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 200,
        "body":json.dumps([
            {
            "username": "bob1",
            "created_on": "2001-01-01T00:00:00Z",
            "review": "holy wow! this newfangled gizmo is so rad!"
            },
            {
            "username": "bob2",
            "created_on": "2003-01-11T00:00:00Z",
            "review": "... this item totally sucks :("
            },
        ])
    }
    actual = gateway.get_reviews_by_listing_id(http, token, 5678)
    assert expected == actual