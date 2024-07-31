import datetime
import urllib3
from mockito import when, mock, verify
from test_utils import DATA_URL, sign_jwt_for_test, DATA_API_KEY
import json
import gateway


def test_create_listing_success():
    address = "500 Fort St, Victoria, BC V8W 1E5"
    http = mock(urllib3.PoolManager())

    mockGeo = mock({
        "status": 200,
    })
    when(mockGeo).json().thenReturn({
        "results": [{
            "position": {
                "lat": 12.3456,
                "lon": 78.9012
            },
            "address": {
                "postalCode": "V8W"
            }
        }]
    })
    when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                       .format(gateway.MAPS_API_KEY, address)).thenReturn(mockGeo)

    response = mock({
        "status": 201,
    })
    when(response).json().thenReturn({
        "listingId": 1234,
        "title": "Chair",
        "price": 100.00,
        "address": "V8W",
        "status": "AVAILABLE",
        "charity": False
    })
    when(http).request("POST", f"{DATA_URL}/create_listing", json={
        "sellerId": 5678,
        "title": "Chair",
        "price": 100.00,
        "latitude": 12.3456,
        "longitude": 78.9012,
        "address": "V8W",
        "status": "AVAILABLE",
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 201,
        "body": json.dumps({
            "listingId": 1234,
            "title": "Chair",
            "price": 100.00,
            "location": "V8W",
            "status": "AVAILABLE",
            "forCharity": False
        }),
    }
    actual = gateway.create_listing(
        http, token, "Chair", 100.00, address, False)
    assert expected == actual


def test_create_listing_fail():
    http = mock(urllib3.PoolManager())

    address = "500 Fort St, Victoria, BC V8W 1E5"

    mockGeo = mock({
        "status": 200,
    })
    when(mockGeo).json().thenReturn({
        "results": [{
            "position": {
                "lat": 12.3456,
                "lon": 78.9012
            },
            "address": {
                "postalCode": "V8W"
            }
        }]
    })
    when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                       .format(gateway.MAPS_API_KEY, address)).thenReturn(mockGeo)

    response = mock({
        "status": 400,
    })

    when(http).request("POST", f"{DATA_URL}/create_listing", json={
        "sellerId": 5678,
        "title": "",
        "price": 100.00,
        "latitude": 12.3456,
        "longitude": 78.9012,
        "address": "V8W",
        "status": "AVAILABLE",
        "charity": True
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })

    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid request"
        }),
    }

    actual = gateway.create_listing(http, token, "", 100.00, address, True)
    assert expected == actual


def test_patch_listing_success():
    http = mock(urllib3.PoolManager())
    address = "500 Fort St, Victoria, BC V8W 1E5"

    mockGeo = mock({
        "status": 200,
    })
    when(mockGeo).json().thenReturn({
        "results": [{
            "position": {
                "lat": 12.3456,
                "lon": 78.9012
            },
            "address": {
                "postalCode": "V8W"
            }
        }]
    })
    when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                       .format(gateway.MAPS_API_KEY, address)).thenReturn(mockGeo)

    lookup_result = mock({
        "status": 200,
    })
    when(lookup_result).json().thenReturn({
        "sellerId": 5678,
        "status": "AVAILABLE",
    })
    when(http).request(
        "GET", f"{DATA_URL}/get_listing?listingId=1111", json=None, headers={
            "X-Api-Key": DATA_API_KEY
        }).thenReturn(lookup_result)

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "listingId": 1234,
    })
    when(http).request("POST", f"{DATA_URL}/update_listing", json={
        "listingId": 1111,
        "title": "Table",
        "price": 10.00,
        "latitude": 12.3456,
        "longitude": 78.9012,
        "address": "V8W",
        "status": "AVAILABLE",
        "charity": None
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 200,
    }
    actual = gateway.update_listing(
        http, token, 1111, "Table", 10.00, "500 Fort St, Victoria, BC V8W 1E5", "AVAILABLE", None, None)
    assert expected == actual


def test_patch_listing_fail():
    http = mock(urllib3.PoolManager())
    address = "500 Fort St, Victoria, BC V8W 1E5"

    mockGeo = mock({
        "status": 200,
    })
    when(mockGeo).json().thenReturn({
        "results": [{
            "position": {
                "lat": 12.3456,
                "lon": 78.9012
            },
            "address": {
                "postalCode": "V8W"
            }
        }]
    })
    when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                       .format(gateway.MAPS_API_KEY, address)).thenReturn(mockGeo)

    lookup_result = mock({
        "status": 200,
    })
    when(lookup_result).json().thenReturn({
        "sellerId": 5678,
        "status": "AVAILABLE",
    })
    when(http).request(
        "GET", f"{DATA_URL}/get_listing?listingId=1111", json=None, headers={
            "X-Api-Key": DATA_API_KEY
        }).thenReturn(lookup_result)

    response = mock({
        "status": 400,
    })
    when(http).request("POST", f"{DATA_URL}/update_listing", json={
        "listingId": 1111,
        "title": "",
        "price": 10.00,
        "latitude": 12.3456,
        "longitude": 78.9012,
        "address": "V8W",
        "status": "AVAILABLE",
        "charity": None
    }, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": "Invalid request"
        }),
    }
    actual = gateway.update_listing(
        http, token, 1111, "", 10.00, address, "AVAILABLE", None, None)
    assert expected == actual


def test_patch_sold_listing():
    http = mock(urllib3.PoolManager())
    address = "500 Fort St, Victoria, BC V8W 1E5"

    mockGeo = mock({
        "status": 200,
    })
    when(mockGeo).json().thenReturn({
        "results": [{
            "position": {
                "lat": 12.3456,
                "lon": 78.9012
            },
            "address": {
                "postalCode": "V8W"
            }
        }]
    })
    when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                       .format(gateway.MAPS_API_KEY, address)).thenReturn(mockGeo)

    lookup_result = mock({
        "status": 200,
    })
    when(lookup_result).json().thenReturn({
        "sellerId": 5678,
        "status": "SOLD",
    })
    when(http).request(
        "GET", f"{DATA_URL}/get_listing?listingId=1111", json=None, headers={
            "X-Api-Key": DATA_API_KEY
        }).thenReturn(lookup_result)

    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 400,
        "body": json.dumps({
            "message": ""
        }),
    }
    actual = gateway.update_listing(
        http, token, 1111, "", 10.00, address, "AVAILABLE", None, None)
    assert expected == actual


def test_patch_other_sellers_listing():
    http = mock(urllib3.PoolManager())
    address = "500 Fort St, Victoria, BC V8W 1E5"

    mockGeo = mock({
        "status": 200,
    })
    when(mockGeo).json().thenReturn({
        "results": [{
            "position": {
                "lat": 12.3456,
                "lon": 78.9012
            },
            "address": {
                "postalCode": "V8W"
            }
        }]
    })
    when(http).request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                       .format(gateway.MAPS_API_KEY, address)).thenReturn(mockGeo)

    lookup_result = mock({
        "status": 200,
    })
    when(lookup_result).json().thenReturn({
        "sellerId": 1234,  # different seller from the userId in token
        "status": "AVAILABLE",
    })
    when(http).request(
        "GET", f"{DATA_URL}/get_listing?listingId=1111", json=None, headers={
            "X-Api-Key": DATA_API_KEY
        }).thenReturn(lookup_result)

    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 401,
    }
    actual = gateway.update_listing(
        http, token, 1111, "", 10.00, address, "AVAILABLE", None, None)
    assert expected == actual


def test_delete_listing_success():
    http = mock(urllib3.PoolManager())
    lookup_result = mock({
        "status": 200,
    })
    when(lookup_result).json().thenReturn({
        "sellerId": 5678,
        "status": "AVAILABLE",
    })
    when(http).request(
        "GET", f"{DATA_URL}/get_listing?listingId=1111", json=None, headers={
            "X-Api-Key": DATA_API_KEY
    }).thenReturn(lookup_result)
    response = mock({
        "status": 200,
    })
    when(http).request("DELETE", f"{DATA_URL}/delete_listing?listingId=1111", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 200,
    }
    actual = gateway.delete_listing(http, token, 1111)
    assert expected == actual


def test_delete_listing_fail():
    http = mock(urllib3.PoolManager())
    response = mock({
        "status": 404,
    })
    lookup_result = mock({
        "status": 200,
    })
    when(lookup_result).json().thenReturn({
        "sellerId": 5678,
        "status": "AVAILABLE",
    })
    when(http).request(
        "GET", f"{DATA_URL}/get_listing?listingId=1111", json=None, headers={
            "X-Api-Key": DATA_API_KEY
    }).thenReturn(lookup_result)
    when(http).request("DELETE", f"{DATA_URL}/delete_listing?listingId=1111", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "Listing not found"
        }),
    }
    actual = gateway.delete_listing(http, token, 1111)
    assert expected == actual


def test_get_sorted_listings_success():
    max_price = "1000.00"
    min_price = None
    sort_by = None
    is_descending = False
    status = "AVAILABLE"

    http = mock(urllib3.PoolManager())

    user_response = mock({
        "status": 200,
    })
    when(user_response).json().thenReturn({
        "location": {
            "lat": 123.456,
            "lng": 789.123,
        }
    })
    when(http).request(
        "GET", f"{DATA_URL}/get_user?userId=5678", json=None, headers={
            "X-Api-Key": DATA_API_KEY
        }).thenReturn(user_response)

    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn([
        {
            "sellerId": 3333,
            "listingId": 1111,
            "title": "Chair",
            "price": 100.00,
            "location": "12.3456,78.9012",
            "address": "V8W",
            "status": "AVAILABLE",
            "for_charity": False,
            "listedAt": "2021-01-01T00:00:00Z",
            "lastUpdatedAt": "2021-01-01T00:00:00Z",
            "charity": False
        },
        {
            "sellerId": 3333,
            "listingId": 1112,
            "title": "Chair",
            "price": 100.00,
            "location": "12.3456,78.9012",
            "address": "V8W",
            "status": "AVAILABLE",
            "for_charity": False,
            "listedAt": "2021-01-01T00:00:00Z",
            "lastUpdatedAt": "2021-01-01T00:00:00Z",
            "charity": True
        },

    ])
    when(http).request("GET", f"{DATA_URL}/get_listings?maxPrice=1000.0&status=AVAILABLE&isDescending=False&lat=123.456&lng=789.123", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 200,
        "body": json.dumps([
            {
                "sellerId": 3333,
                "listingId": 1111,
                "title": "Chair",
                "price": 100.00,
                "location": "V8W",
                "status": "AVAILABLE",
                "forCharity": False,
                "listedAt": "2021-01-01T00:00:00Z",
                "lastUpdatedAt": "2021-01-01T00:00:00Z",
            },
            {
                "sellerId": 3333,
                "listingId": 1112,
                "title": "Chair",
                "price": 100.00,
                "location": "V8W",
                "status": "AVAILABLE",
                "forCharity": True,
                "listedAt": "2021-01-01T00:00:00Z",
                "lastUpdatedAt": "2021-01-01T00:00:00Z",
            },
        ])
    }
    actual = gateway.get_sorted_listings(
        http, token, max_price, min_price, status, sort_by, is_descending)
    assert expected == actual


def test_get_sorted_listings_fail():
    status = "AVAILABLE"
    min_price = None
    max_price = None
    sort_by = "created_on"
    is_descending = False

    http = mock(urllib3.PoolManager())

    user_response = mock({
        "status": 200,
    })
    when(user_response).json().thenReturn({
        "location": {
            "lat": 123.456,
            "lng": 789.123,
        }
    })
    when(http).request(
        "GET", f"{DATA_URL}/get_user?userId=5678", json=None, headers={
            "X-Api-Key": DATA_API_KEY
        }).thenReturn(user_response)

    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"{DATA_URL}/get_listings?status=AVAILABLE&sortBy=created_on&isDescending=False&lat=123.456&lng=789.123", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 200,
        "body": json.dumps([]),
    }
    actual = gateway.get_sorted_listings(
        http, token, max_price, min_price, status, sort_by, is_descending)
    assert expected == actual


def test_get_listing_by_id_success():
    http = mock(urllib3.PoolManager())
    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn({
        "sellerId": 3333,
        "listingId": 1111,
        "title": "Chair",
        "price": 100.00,
        "location": "12.3456,78.9012",
        "address": "V8W",
        "status": "AVAILABLE",
        "for_charity": False,
        "listedAt": "2021-01-01T00:00:00Z",
        "lastUpdatedAt": "2021-01-01T00:00:00Z",
        "charity": False
    })
    when(http).request("GET", f"{DATA_URL}/get_listing?listingId=1111", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 200,
        "body": json.dumps({
            "sellerId": 3333,
            "listingId": 1111,
            "title": "Chair",
            "price": 100.00,
            "location": "V8W",
            "status": "AVAILABLE",
            "forCharity": False,
            "listedAt": "2021-01-01T00:00:00Z",
            "lastUpdatedAt": "2021-01-01T00:00:00Z",
        })
    }
    actual = gateway.get_listing_by_id(http, token, 1111)
    assert expected == actual


def test_get_listing_by_id_fail():
    http = mock(urllib3.PoolManager())
    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"{DATA_URL}/get_listing?listingId=1234", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 404,
        "body": json.dumps({
            "message": "Listing not found"
        }),
    }
    actual = gateway.get_listing_by_id(http, token, 1234)
    assert expected == actual


def test_get_my_listings_success():
    http = mock(urllib3.PoolManager())
    response = mock({
        "status": 200,
    })
    when(response).json().thenReturn([
        {
            "sellerId": 3333,
            "listingId": 1111,
            "title": "Chair",
            "price": 100.00,
            "location": "12.3456,78.9012",
            "address": "V8W",
            "status": "AVAILABLE",
            "for_charity": False,
            "listedAt": "2021-01-01T00:00:00Z",
            "lastUpdatedAt": "2021-01-01T00:00:00Z",
            "charity": False
        },
        {
            "sellerId": 3333,
            "listingId": 1112,
            "title": "Chair",
            "price": 100.00,
            "location": "12.3456,78.9012",
            "address": "V8W",
            "status": "AVAILABLE",
            "for_charity": False,
            "listedAt": "2021-01-01T00:00:00Z",
            "lastUpdatedAt": "2021-01-01T00:00:00Z",
            "charity": True
        },

    ])
    when(http).request("GET", f"{DATA_URL}/get_listing_by_seller?userId={5678}", json=None, headers={
        "X-Api-Key": DATA_API_KEY,
    }).thenReturn(response)
    token = sign_jwt_for_test({
        "uid": 5678
    })
    expected = {
        "statusCode": 200,
        "body": json.dumps([
            {
                "sellerId": 3333,
                "listingId": 1111,
                "title": "Chair",
                "price": 100.00,
                "location": "V8W",
                "status": "AVAILABLE",
                "forCharity": False,
                "listedAt": "2021-01-01T00:00:00Z",
                "lastUpdatedAt": "2021-01-01T00:00:00Z",
            },
            {
                "sellerId": 3333,
                "listingId": 1112,
                "title": "Chair",
                "price": 100.00,
                "location": "V8W",
                "status": "AVAILABLE",
                "forCharity": True,
                "listedAt": "2021-01-01T00:00:00Z",
                "lastUpdatedAt": "2021-01-01T00:00:00Z",
            },
        ])
    }
    actual = gateway.get_my_listings(http, token)
    assert expected == actual


def test_get_my_listings_auth_fail():
    http = mock(urllib3.PoolManager())

    expected = {
        "statusCode": 401,
    }

    actual = gateway.get_my_listings(http, None)
    assert expected == actual
