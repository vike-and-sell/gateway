import datetime
import urllib3
from mockito import when, mock, verify
from test_utils import DATA_URL, sign_jwt_for_test, DATA_API_KEY
import json
import gateway

# def test_create_listing_success():
#     listing_data = {        
#         "title": "Chair",
#         "price": 100.00,
#         "latitiude": 12.3456,
#         "longitude": 78.9012, 
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",}

#     http = mock(urllib3.PoolManager())
#     response = mock({
#         "status": 201,
#     })
#     when(response).json().thenReturn({
#         "listingId": 1234,
#     })
#     when(http).request("POST", "f"http://{DATA_URL}/create_listing", json={
#         "sellerId": 5678,
#         "title": "Chair",
#         "price": 100.00,
#         "latitiude": 12.3456,
#         "longitude": 78.9012, 
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
    
#     }, headers={
#         "X-Api-Key": DATA_API_KEY,
#     }).thenReturn(response)
#     token = sign_jwt_for_test({
#         "uid": 5678
#     })
#     expected = {
#         "statusCode": 201,
#         "body": json.dumps({
#             "listingId": 1234,
#         })
#     }
#     actual = gateway.create_listing(http, token, listing_data)
#     assert expected == actual

# def test_create_listing_fail():
#     http = mock(urllib3.PoolManager())

#     response = mock({
#         "status": 400,
#     })
    
#     when(http).request("POST", f"http://{DATA_URL}/create_listing", json={
#         "sellerId": 5678,
#         "title": "",
#         "price": 100.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
    
#     }, headers={
#         "X-Api-Key": DATA_API_KEY,
#     }).thenReturn(response)
#     token = sign_jwt_for_test({
#         "uid": 5678
#     })

#     expected = {
#         "statusCode": 400,
#         "body": json.dumps({
#             "message": "Invalid request"
#         }),
#     }

#     actual = gateway.create_listing(http, token, {
#         "title": "",
#         "price": 100.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
#     })
#     assert expected == actual

# def test_patch_listing_success():
#     updated_listing_data = {        
#         "sellerId": 5678,
#         "title": "Table",
#         "price": 10.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
#     }

#     http = mock(urllib3.PoolManager())
#     response = mock({
#         "status": 200,
#     })
#     when(response).json().thenReturn({
#         "listingId": 1234,
#     })

# # update so that listingId is part of the updated listing data

#     when(http).request("POST", f"http://{DATA_URL}/update_listing?listingId=1111", json={
#         "sellerId": 5678,
#         "title": "Table",
#         "price": 10.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
    
#     }, headers={
#         "X-Api-Key": DATA_API_KEY,
#     }).thenReturn(response)
#     token = sign_jwt_for_test({
#         "uid": 5678
#     })
#     expected = {
#         "statusCode": 200,
#     }
#     actual = gateway.update_listing(http, token, 1111, updated_listing_data)
#     assert expected == actual

# def test_patch_listing_fail():
#     updated_listing_data = { 
#         "sellerId": 5678,  
#         "title": "",
#         "price": 10.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
#     }

#     http = mock(urllib3.PoolManager())
#     response = mock({
#         "status": 400,
#     })

# # update so that listingId is part of the updated listing data

#     when(http).request("POST", f"http://{DATA_URL}/update_listing?listingId=1111", json={
#         "sellerId": 5678,
#         "title": "",
#         "price": 10.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
    
#     }, headers={
#         "X-Api-Key": DATA_API_KEY,
#     }).thenReturn(response)
#     token = sign_jwt_for_test({
#         "uid": 5678
#     })
#     expected = {
#         "statusCode": 400,
#         "body": json.dumps({
#             "message": "Invalid request"
#         }),
#     }
#     actual = gateway.update_listing(http, token, 1111, updated_listing_data)
#     assert expected == actual

def test_delete_listing_success():
    http = mock(urllib3.PoolManager())
    response = mock({
        "status": 200,
    })
    when(http).request("DELETE", f"http://{DATA_URL}/delete_listing?listingId=1111", json=None, headers={
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
    when(http).request("DELETE", f"http://{DATA_URL}/delete_listing?listingId=1111", json=None, headers={
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

# def test_get_sorted_listings_success():
#     keywords = "status=AVAILABLE"

#     http = mock(urllib3.PoolManager())
#     response = mock({
#         "status": 200,
#     })
#     when(response).json().thenReturn([
#         {
#         "sellerId": 3333,
#         "listingId": 1111,
#         "title": "Chair",
#         "price": 100.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
#         "listedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         "lastUpdatedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         },
#         {
#         "sellerId": 3333,
#         "listingId": 1111,
#         "title": "Chair",
#         "price": 100.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
#         "listedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         "lastUpdatedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         },

#     ])
#     when(http).request("GET", f"http://{DATA_URL}/get_listings?status=AVAILABLE", json=None, headers={
#         "X-Api-Key": DATA_API_KEY,
#     }).thenReturn(response)
#     token = sign_jwt_for_test({
#         "uid": 5678
#     })
#     expected = {
#         "statusCode": 200,
#         "body": json.dumps([
#             {
#             "sellerId": 3333,
#             "listingId": 1111,
#             "title": "Chair",
#             "price": 100.00,
#             "location": "V8W",
#             "status": "AVAILABLE",
#             "listedAt": "2021-01-01T00:00:00Z",
#             "lastUpdatedAt": "2021-01-01T00:00:00Z",
#             },
#             {
#             "sellerId": 3333,
#             "listingId": 1111,
#             "title": "Chair",
#             "price": 100.00,
#             "location": "V8W",
#             "status": "AVAILABLE",
#             "listedAt": "2021-01-01T00:00:00Z",
#             "lastUpdatedAt": "2021-01-01T00:00:00Z",
#             },
#         ])
#     }
#     actual = gateway.get_sorted_listings(http, token, keywords)
#     assert expected == actual

def test_get_sorted_listings_fail():
    keywords = "status=AVAILABLE"

    http = mock(urllib3.PoolManager())
    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"http://{DATA_URL}/get_listings?status=AVAILABLE", json=None, headers={
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
    actual = gateway.get_sorted_listings(http, token, keywords)
    assert expected == actual

# def test_get_listing_by_id_success():
#     http = mock(urllib3.PoolManager())
#     response = mock({
#         "status": 200,
#     })
#     when(response).json().thenReturn({
#         "sellerId": 3333,
#         "listingId": 1111,
#         "title": "Chair",
#         "price": 100.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
#         "listedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         "lastUpdatedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#     })
#     when(http).request("GET", f"http://{DATA_URL}/get_listing?listingId=1111", json=None, headers={
#         "X-Api-Key": DATA_API_KEY,
#     }).thenReturn(response)
#     token = sign_jwt_for_test({
#         "uid": 5678
#     })
#     expected = {
#         "statusCode": 200,
#         "body": json.dumps({
#             "sellerId": 3333,
#             "listingId": 1111,
#             "title": "Chair",
#             "price": 100.00,
#             "location": "V8W",
#             "status": "AVAILABLE",
#             "listedAt": "2021-01-01T00:00:00Z",
#             "lastUpdatedAt": "2021-01-01T00:00:00Z",
#         })
#     }
#     actual = gateway.get_listing_by_id(http, token, 1111)
#     assert expected == actual

def test_get_listing_by_id_fail():
    http = mock(urllib3.PoolManager())
    response = mock({
        "status": 404,
    })
    when(http).request("GET", f"http://{DATA_URL}/get_listing?listingId=1234", json=None, headers={
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

# def test_get_my_listings_success():
#     http = mock(urllib3.PoolManager())
#     response = mock({
#         "status": 200,
#     })
#     when(response).json().thenReturn([
#         {
#         "sellerId": 3333,
#         "listingId": 1111,
#         "title": "Chair",
#         "price": 100.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
#         "listedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         "lastUpdatedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         },
#         {
#         "sellerId": 3333,
#         "listingId": 1111,
#         "title": "Chair",
#         "price": 100.00,
#         "location": "12.3456,78.9012",
#         "address": "500 Fort St, Victoria, BC V8W 1E5",
#         "status": "AVAILABLE",
#         "listedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         "lastUpdatedAt": datetime.datetime.fromisoformat("2021-01-01T00:00:00Z"),
#         },

#     ])
#     when(http).request("GET", f"http://{DATA_URL}/get_listing_by_seller?userId={5678}", json=None, headers={
#         "X-Api-Key": DATA_API_KEY,
#     }).thenReturn(response)
#     token = sign_jwt_for_test({
#         "uid": 5678
#     })
#     expected = {
#         "statusCode": 200,
#         "body": json.dumps([
#             {
#             "sellerId": 3333,
#             "listingId": 1111,
#             "title": "Chair",
#             "price": 100.00,
#             "location": "V8W",
#             "status": "AVAILABLE",
#             "listedAt": "2021-01-01T00:00:00Z",
#             "lastUpdatedAt": "2021-01-01T00:00:00Z",
#             },
#             {
#             "sellerId": 3333,
#             "listingId": 1111,
#             "title": "Chair",
#             "price": 100.00,
#             "location": "V8W",
#             "status": "AVAILABLE",
#             "listedAt": "2021-01-01T00:00:00Z",
#             "lastUpdatedAt": "2021-01-01T00:00:00Z",
#             },
#         ])
#     }
#     actual = gateway.get_my_listings(http, token)
#     assert expected == actual

def test_get_my_listings_auth_fail():
    http = mock(urllib3.PoolManager())

    expected = {
        "statusCode": 401,
    }

    actual = gateway.get_my_listings(http, None)
    assert expected == actual

