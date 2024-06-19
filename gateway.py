import os
import json
import datetime

import jwt
import jwt.exceptions
import jwt.utils
import pyap
import urllib3

DATA_URL = os.environ["DATA_URL"]
DATA_API_KEY = os.environ["DATA_API_KEY"]
JWT_SECRET = os.environ["JWT_SECRET_KEY"]


def address_to_postal_code(address):
    parsed = pyap.parse(address, country="CA")
    truncated_postal_code = parsed[0].postal_code[0:3]
    return truncated_postal_code


def resolve_credentials(auth_token: str):
    try:
        result: dict = jwt.decode(auth_token, JWT_SECRET, algorithms="HS256")
        return result.get("uid")
    except Exception:
        return None


def make_ok_response(body=None, headers: dict = None):
    result = {
        "statusCode": 200,
    }

    if headers:
        result["headers"] = headers,

    if body:
        result["body"] = json.dumps(body)

    return result


def make_invalid_request_response(message: str = ""):
    return {
        "statusCode": 400,
        "body": json.dumps({
            "message": message
        })
    }


def make_unauthorized_response():
    return {
        "statusCode": 401,
    }


def make_not_found_response(message: str = ""):
    return {
        "statusCode": 404,
        "body": json.dumps({
            "message": message
        }),
    }


def make_internal_error_response():
    return {
        "statusCode": 500,
    }


def execute_data_request(http: urllib3.PoolManager, path, method, body):
    headers = {
        "X-Api-Key": DATA_API_KEY,
    }
    return http.request(method, f"http://{DATA_URL}{path}", body=body, headers=headers)


def execute_data_get(http, path):
    return execute_data_request(http, path, "GET", None)


def execute_data_post(http, path, body):
    return execute_data_request(http, path, "POST", body)


def get_user_by_id(http: urllib3.PoolManager, auth_token, user_id):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = execute_data_get(http, f"/get_user?userId={user_id}")
    if result.status == 200:
        try:
            data = result.json()
            username = data["username"]
            full_address = data["address"]
            joining_date: datetime.datetime = data["joining_date"]
            items_sold = data["items_sold"]
            items_purchased = data["items_purchased"]

            safe_address = address_to_postal_code(full_address)

            return make_ok_response(body={
                "username": username,
                "location": safe_address,
                "joiningDate": joining_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "itemsSold": [str(x) for x in items_sold],
                "itemsPurchased": [str(x) for x in items_purchased],
            })
        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()
    elif result.status == 404:
        return make_not_found_response("User not found")

    return make_internal_error_response()


def get_user_by_auth_token(http, auth_token):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    return get_user_by_id(http, auth_token, creds)


def update_user_by_id(http, auth_token, user_id, address):
    creds = resolve_credentials(auth_token)
    if not creds or creds != user_id:
        return make_unauthorized_response()

    parsed_address = pyap.parse(address, country="CA")
    if len(parsed_address) == 0:
        return make_invalid_request_response("Invalid address")

    result = execute_data_post(http, "/update_user", {
        "userId": user_id,
        "address": parsed_address[0].full_address,
    })

    if result.status == 200:
        return make_ok_response()
    elif result.status == 400:
        return make_invalid_request_response("Invalid request")

    return make_internal_error_response()


def get_search_history_by_id(http, auth_token, user_id):
    creds = resolve_credentials(auth_token)
    if not creds or creds != user_id:
        return make_unauthorized_response()

    result = execute_data_get(http, f"/get_searches?userId={user_id}")

    if result.status == 200:
        data = result.json()
        return make_ok_response(body=data["searches"])
    elif result.status == 404:
        return make_not_found_response()

    return make_internal_error_response()

def get_ratings_by_listing_id(http, auth_token, listing_id):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()
    if not isinstance(listing_id, int):
        return make_invalid_request_response("Invalid arg types")

    result = execute_data_get(http, f"/get_ratings?listingId={listing_id}")

    if result.status == 200:
        data = result.json()
        body = []
        for object in data:
            body.append({
                "username": object["username"],
                "created_on": object["created_on"].isoformat(),
                "rating": object["rating"]
            })
        return make_ok_response(body=body)
    if result.status  == 404:
        return make_not_found_response("Listing not found")

    return make_internal_error_response()

def post_rating_by_listing_id(http, auth_token, listing_id, rating):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()
    if not isinstance(listing_id, int) or not isinstance(rating, int):
        return make_invalid_request_response("Invalid arg types")
    if rating < 1 or rating > 5:
        return make_invalid_request_response("Rating should be between 1 and 5")

    result = execute_data_post(http, f"/create_rating", {
        "listingId": listing_id,
        "rating": rating
    })

    if result.status == 200:
        return make_ok_response()
    if result.status  == 404:
        return make_not_found_response("Listing not found")

    return make_internal_error_response()

def get_reviews_by_listing_id(http, auth_token, listing_id):
    creds = resolve_credentials(auth_token)

    if not creds:
        return make_unauthorized_response()
    if not isinstance(listing_id, int):
        return make_invalid_request_response("Invalid arg types")

    result = execute_data_get(http, f"/get_reviews?listingId={listing_id}")

    if result.status == 200:
        data = result.json()
        body = []
        for object in data:
            body.append({
                "username": object["username"],
                "created_on": object["created_on"].isoformat(),
                "review": object["review"]
            })
        return make_ok_response(body=body)
    if result.status  == 404:
        return make_not_found_response("Listing not found")

    return make_internal_error_response()

def post_review_by_listing_id(http, auth_token, listing_id, review):
    creds = resolve_credentials(auth_token)

    if not creds:
        return make_unauthorized_response()
    if not isinstance(listing_id, int) or not isinstance(review, str):
        return make_invalid_request_response("Invalid arg types")

    result = execute_data_post(http, f"/create_review", {
        "listingId": listing_id,
        "review": review
    })

    if result.status == 200:
        return make_ok_response()
    

def not_implemented():
    return {
        "statusCode": 501,
        "body": json.dumps({
            "message": "NOT IMPLEMENTED"
        })
    }
