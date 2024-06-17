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

def test_get_ratings_success(setup_module):
    http, token = setup_module

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

def test_get_ratings_does_not_exist(setup_module):
    http, token = setup_module

    response = mock({
        "status": 404,
    })
    when(http).request("GET", "http://test/get_ratings?listingId=5678", body=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "Listing not found"
        })
    }
    
    actual = gateway.get_ratings_by_listing_id(http, token, 5678)
    assert expected == actual

def test_get_ratings_unauthorized(setup_module):
    http, _ = setup_module

    expected = {
        "statusCode": 401,
    }
    actual = gateway.get_ratings_by_listing_id(http, None, 5678)
    assert expected == actual

    actual = gateway.get_ratings_by_listing_id(http, sign_jwt_for_test({}), 5678)
    assert expected == actual

def test_get_ratings_invalid_type(setup_module):
    http, token = setup_module

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid arg types"
        })
    }

    actual = gateway.get_ratings_by_listing_id(http, token, "not number")
    assert expected == actual
    actual = gateway.get_ratings_by_listing_id(http, token, [1, 2, 3, 4])
    assert expected == actual

def test_post_rating_success(setup_module):
    http, token = setup_module
    listing_id = 5678
    rating = 5

    response = mock({
        "status": 200,
    })

    when(http).request("POST", "http://test/create_rating", body={
        "listingId": listing_id,
        "rating": rating
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 200,
    }
    actual = gateway.post_rating_by_listing_id(http, token, listing_id, rating)
    assert expected == actual

def test_post_listing_not_found(setup_module):
    http, token = setup_module
    listing_id = 5678
    rating = 5

    response = mock({
        "status": 404,
    })

    when(http).request("POST", "http://test/create_rating", body={
        "listingId": listing_id,
        "rating": rating
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "Listing not found"
        })
    }
    actual = gateway.post_rating_by_listing_id(http, token, listing_id, rating)
    assert expected == actual

def test_post_listing_illegal_rating(setup_module):
    http, token = setup_module

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Rating should be between 1 and 5"
        })
    }
    actual = gateway.post_rating_by_listing_id(http, token, 5678, 0)
    assert expected == actual
    actual = gateway.post_rating_by_listing_id(http, token, 5678, 6)
    assert expected == actual

def test_get_ratings_invalid_type(setup_module):
    http, token = setup_module

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid arg types"
        })
    }

    actual = gateway.post_rating_by_listing_id(http, token, 12, 6.5)
    assert expected == actual
    actual = gateway.post_rating_by_listing_id(http, token, [1, 2, 3, 4], 2)
    assert expected == actual