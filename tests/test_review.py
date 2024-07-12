import datetime
from mockito import when, mock, verify
import pytest
import urllib3
import json
from test_utils import DATA_URL, sign_jwt_for_test, DATA_API_KEY

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
            "created_on": "2001-01-01T00:00:00+00:00",
            "review": "holy wow! this newfangled gizmo is so rad!"
        },
        {
            "username": "bob2",
            "created_on": "2003-01-11T00:00:00+00:00",
            "review": "... this item totally sucks :("
        },
    ])
    when(http).request("GET", f"{DATA_URL}/get_reviews?listingId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 200,
        "body": json.dumps([
            {
                "username": "bob1",
                "created_on": "2001-01-01T00:00:00+00:00",
                "review": "holy wow! this newfangled gizmo is so rad!"
            },
            {
                "username": "bob2",
                "created_on": "2003-01-11T00:00:00+00:00",
                "review": "... this item totally sucks :("
            },
        ])
    }
    actual = gateway.get_reviews_by_listing_id(http, token, 5678)
    assert expected == actual


def test_get_reviews_listing_not_found(setup_module):
    http, token = setup_module

    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"{DATA_URL}/get_reviews?listingId=5678", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "Listing not found"
        })
    }

    actual = gateway.get_reviews_by_listing_id(http, token, 5678)
    assert expected == actual


def test_get_reviews_invalid_type(setup_module):
    http, token = setup_module

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid args"
        })
    }

    actual = gateway.get_reviews_by_listing_id(http, token, "not number")
    assert expected == actual
    actual = gateway.get_reviews_by_listing_id(http, token, [1, 2, 3, 4])
    assert expected == actual


def test_post_review_success(setup_module):
    http, token = setup_module

    response = mock({
        "status": 200
    })
    when(http).request("POST", f"{DATA_URL}/create_review", json={
        "listingId": 5678,
        "review": "Ok, now this is awesome!",
        "userId": 1234,
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)

    expected = {
        "statusCode": 200
    }

    actual = gateway.post_review_by_listing_id(
        http, token, 5678, "Ok, now this is awesome!")
    assert expected == actual


def test_post_review_unauthorized(setup_module):
    http, _ = setup_module

    expected = {
        "statusCode": 401,
    }
    actual = gateway.post_review_by_listing_id(http, None, 5678, "Terrible.")

    assert expected == actual

    actual = gateway.post_review_by_listing_id(
        http, sign_jwt_for_test({}), 5678, "Terrible.")
    assert expected == actual


def test_post_review_invalid_type(setup_module):
    http, token = setup_module

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid args"
        })
    }

    actual = gateway.post_review_by_listing_id(
        http, token, "text", "Terrible.")
    assert expected == actual
    actual = gateway.post_review_by_listing_id(
        http, token, 5678, {"generic": 1234})
    assert expected == actual
