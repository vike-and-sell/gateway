import os
import json
import datetime
import re

import jwt
import jwt.exceptions
import jwt.utils
import pyap
import urllib3
import hashlib

DATA_URL = os.environ["DATA_URL"]
DATA_API_KEY = os.environ["DATA_API_KEY"]
JWT_SECRET = os.environ["JWT_SECRET_KEY"]
MAPS_API_KEY = os.environ["MAPS_API_KEY"]


def parse_address(address):
    parsed = pyap.parse(address, country="CA")

    if len(parsed) == 0:
        return None

    if len(parsed[0].postal_code[0:3]) < 3:
        return None

    return parsed[0]


def address_to_latlng(http, address):
    geocode_raw = http.request("GET", "https://atlas.microsoft.com/search/address/json?&subscription-key={}&api-version=1.0&language=en-US&query={}"
                               .format(MAPS_API_KEY, address))

    print(geocode_raw)
    if geocode_raw.status == 200:
        geocode = geocode_raw.json()
        pos = geocode["results"][0]["position"]
        lat = pos["lat"]
        lng = pos["lon"]
        return (lat, lng)

    return None


def address_to_postal_code(address):
    print(address)
    parsed = pyap.parse(address, country="CA")
    truncated_postal_code = parsed[0].postal_code[0:3]
    return truncated_postal_code


def resolve_credentials(auth_token: str):
    try:
        result: dict = jwt.decode(auth_token, JWT_SECRET, algorithms="HS256")
        return result.get("uid")
    except Exception:
        return None


def make_ok_response(body=None, headers: dict = None, auth: dict = None):
    result = {
        "statusCode": 200,
    }

    if auth is not None:
        result["auth"] = auth

    if body is not None:
        result["body"] = json.dumps(body)

    return result


def make_created_response(body=None, headers: dict = None, auth: dict = None):
    result = {
        "statusCode": 201,
    }

    if auth is not None:
        result["auth"] = auth

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
    return http.request(method, f"http://{DATA_URL}{path}", json=body, headers=headers)


def execute_data_get(http, path):
    return execute_data_request(http, path, "GET", None)


def execute_data_post(http, path, body):
    return execute_data_request(http, path, "POST", body)


def execute_data_delete(http, path):
    return execute_data_request(http, path, "DELETE", None)


def get_user_by_id(http: urllib3.PoolManager, auth_token, user_id):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = execute_data_get(http, f"/get_user?userId={user_id}")
    if result.status == 200:
        try:
            print('start of data processing')
            data = result.json()
            print('parsed json')
            username = data["username"]
            full_address = data["address"]
            joining_date = data["joining_date"]
            items_sold = data["items_sold"]
            items_purchased = data["items_purchased"]

            print(type(joining_date))
            print('parsing address to postal code')

            safe_address = address_to_postal_code(full_address)

            print(f'safe address: {safe_address}')

            return make_ok_response(body={
                "userId": user_id,
                "username": username,
                "location": safe_address,
                "joiningDate": joining_date,
                "itemsSold": [str(x) for x in items_sold],
                "itemsPurchased": [str(x) for x in items_purchased],
            })
        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            print(e)
            make_internal_error_response()
    elif result.status == 404:
        return make_not_found_response("User not found")

    return make_internal_error_response()


def get_user_by_auth_token(http, auth_token):
    print("getting user by auth token")
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    print(f"userid: {creds}")

    return get_user_by_id(http, auth_token, creds)


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
    if result.status == 404:
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
    if result.status == 404:
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
    if result.status == 404:
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


def update_user_by_id(http, auth_token, user_id, address):
    creds = resolve_credentials(auth_token)
    if not creds or creds != user_id:
        return make_unauthorized_response()

    print(f"userId: {user_id}")

    parsed_address = parse_address(address)
    if parsed_address is None:
        return make_invalid_request_response("Invalid address")

    full_address = parsed_address.full_address

    geocode_result = address_to_latlng(http, full_address)
    if geocode_result is None:
        return make_internal_error_response()

    lat, lng = geocode_result

    result = execute_data_post(http, "/update_user", {
        "userId": user_id,
        "address": full_address,
        "location": {
            "lat": lat,
            "lng": lng,
        },
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

    result = execute_data_get(http, f"/get_search_history?userId={user_id}")

    if result.status == 200:
        data = result.json()
        print(data)
        return make_ok_response(body=[x['search_text'] for x in data])
    elif result.status == 404:
        return make_not_found_response()

    return make_internal_error_response()


def get_listing_by_id(http: urllib3.PoolManager, auth_token, listing_id):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    print(f"listingId: {listing_id}")
    result = execute_data_get(http, f"/get_listing?listingId={listing_id}")
    if result.status == 200:
        try:
            data = result.json()
            sellerId = data["sellerId"]
            listingId = data["listingId"]
            title = data["title"]
            price = data["price"]
            full_address = data["address"]
            status = data["status"]
            listedAt: datetime.datetime = data["listedAt"]
            lastUpdatedAt: datetime.datetime = data["lastUpdatedAt"]

            safe_address = address_to_postal_code(full_address)

            return make_ok_response(body={
                "sellerId": sellerId,
                "listingId": listingId,
                "title": title,
                "price": price,
                "location": safe_address,
                "status": status,
                "listedAt": listedAt,
                "lastUpdatedAt": lastUpdatedAt,
            })
        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()
    elif result.status == 404:
        return make_not_found_response("Listing not found")

    return make_internal_error_response()


def get_my_listings(http: urllib3.PoolManager, auth_token):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = execute_data_get(http, f"/get_listing_by_seller?userId={creds}")
    if result.status == 200:
        try:
            data = result.json()

            listings_list = []

            for listing in data:
                sellerId = listing["sellerId"]
                listingId = listing["listingId"]
                title = listing["title"]
                price = listing["price"]
                full_address = listing["address"]
                safe_address = address_to_postal_code(full_address)
                status = listing["status"]
                listedAt: datetime.datetime = listing["listedAt"]
                lastUpdatedAt: datetime.datetime = listing["lastUpdatedAt"]

                listings_list.append({
                    "sellerId": sellerId,
                    "listingId": listingId,
                    "title": title,
                    "price": price,
                    "location": safe_address,
                    "status": status,
                    "listedAt": listedAt,
                    "lastUpdatedAt": lastUpdatedAt
                })

            return make_ok_response(body=listings_list)

        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()
    elif result.status == 404:
        return make_not_found_response("Listing not found")

    return make_internal_error_response()


def get_sorted_listings(http: urllib3.PoolManager, auth_token, keywords):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = execute_data_get(http, f"/get_listings?{keywords}")
    if result.status == 200:
        try:
            data = result.json()

            listings_list = []

            for listing in data:
                sellerId = listing["sellerId"]
                listingId = listing["listingId"]
                title = listing["title"]
                price = listing["price"]
                full_address = listing["address"]
                safe_address = address_to_postal_code(full_address)
                status = listing["status"]
                listedAt: datetime.datetime = listing["listedAt"]
                lastUpdatedAt: datetime.datetime = listing["lastUpdatedAt"]

                listings_list.append({
                    "sellerId": sellerId,
                    "listingId": listingId,
                    "title": title,
                    "price": price,
                    "location": safe_address,
                    "status": status,
                    "listedAt": listedAt,
                    "lastUpdatedAt": lastUpdatedAt,
                })

            return make_ok_response(body=listings_list)

        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()
    elif result.status == 404:
        return make_not_found_response("Listing not found")

    return make_internal_error_response()


def create_listing(http: urllib3.PoolManager, auth_token, listing_data):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    address = listing_data["address"]
    lat, lng = address_to_latlng(http, address)

    result = execute_data_post(http, f"/create_listing", {
        "sellerId": creds,
        "title": listing_data["title"],
        "price": listing_data["price"],
        "latitude": lat,
        "longitude": lng,
        "address": listing_data["address"],
        "status": listing_data["status"],
    })
    if result.status == 201:
        try:
            data = result.json()
            return make_created_response(body={
                "listingId": data["listingId"],
            })

        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()
    elif result.status == 400:
        return make_invalid_request_response("Invalid request")
    return make_internal_error_response()


def update_listing(http: urllib3.PoolManager, auth_token, listing_id, updated_listing_data):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    updated_listing_data['listingId'] = listing_id
    result = execute_data_post(
        http, f"/update_listing", updated_listing_data)
    if result.status == 200:
        try:
            data = result.json()
            return make_ok_response()

        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()
    elif result.status == 400:
        return make_invalid_request_response("Invalid request")


def delete_listing(http: urllib3.PoolManager, auth_token, listing_id):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = execute_data_delete(
        http, f"/delete_listing?listingId={listing_id}")
    if result.status == 200:
        try:
            data = result.json()
            return make_ok_response()

        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()
    elif result.status == 404:
        return make_not_found_response("Listing not found")
    elif result.status == 400:
        return make_invalid_request_response("Invalid request")


def get_chats(http, auth_token):
    creds = resolve_credentials(auth_token)

    if not creds:
        return make_unauthorized_response()

    result = execute_data_get(http, f"/get_chats?userId={creds}")

    if result.status == 200:
        data = result.json()
        body = [str(x) for x in data]
        return make_ok_response(body)
    if result.status == 404:
        return make_ok_response([])

    return make_internal_error_response()


def create_chat(http, auth_token, listingId):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = execute_data_get(http, f"/get_listing?listingId={listingId}")
    if result.status == 404:
        return make_not_found_response()
    elif result.status != 200:
        return make_internal_error_response()

    try:
        data = result.json()
        sellerId = data["sellerId"]
        result = execute_data_post(http, "/create_chat", {
            "listingId": listingId,
            "sellerId": sellerId,
            "buyerId": creds
        })
        if result.status == 200:
            data = result.json()
            chatId = data["chatId"]
            return make_created_response(body={
                "chatId": chatId
            })

    except Exception as e:
        print(e)

    return make_internal_error_response()


def get_messages(http, auth_token, chat_id):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = execute_data_get(http, f"/get_messages?chatId={chat_id}")

    if result.status == 200:
        data = result.json()
        print(data)
        messages = [{
            "messageId": str(x["message_id"]),
            "senderId": str(x["sender_id"]),
            "content": str(x["message_content"]),
            "timestamp": x["created_on"]
        } for x in data]
        return make_ok_response({
            "messages": messages
        })
    if result.status == 404:
        return make_not_found_response("chatId does not exist")

    return make_internal_error_response()


def get_chat_preview(http, auth_token, chat_id):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    chat_info = execute_data_get(http, f"/get_chat_info?chatId={chat_id}")
    if chat_info.status == 200:
        # only execute the second query if the first one succeeds to save processing power
        last_message_result = execute_data_get(
            http, f"/get_last_message_timestamp?chatId={chat_id}")
        if last_message_result.status == 200:
            chat_json = chat_info.json()
            print(chat_json)
            last_message_json = last_message_result.json()
            users = [str(chat_json["seller"]), str(chat_json["buyer"])]
            listing_id = str(chat_json["listing_id"])
            last_message_time = last_message_json["timestamp"]
            return make_ok_response({
                "users": users,
                "listingId": listing_id,
                "lastMessageTime": last_message_time
            })
        else:
            return make_internal_error_response()
    elif chat_info.status == 404:
        return make_not_found_response("chatId not found")

    return make_internal_error_response()


def write_message(http, auth_token, chat_id, content) -> int:
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    chat_info = execute_data_get(http, f"/get_chat_info?chatId={chat_id}")
    if chat_info.status == 200:
        data = chat_info.json()
        seller = data["seller"]
        buyer = data["buyer"]
        # first make sure that this account is allowed
        # to send messages in the chat
        if creds != seller and creds != buyer:
            return make_unauthorized_response()

        result = execute_data_post(http, f"/create_message", {
            "chatId": chat_id,
            "content": content,
            "senderId": creds
        })
        if result.status == 200:
            return make_ok_response()
        else:
            return make_internal_error_response()

    elif chat_info.status == 404:
        return make_not_found_response("chatId not found")

    return make_internal_error_response()


def get_search(http, auth_token, q):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = http.request("GET", f"http://serber.ddns.net:32500/search?q={q}")
    if result.status == 200:
        try:
            data = result.json()
            listings_list = []

            for listing in data:
                sellerId = listing["seller_id"]
                listingId = listing["listing_id"]
                title = listing["title"]
                price = listing["price"]
                full_address = listing["address"]
                safe_address = address_to_postal_code(full_address)
                status = listing["status"]
                listedAt = listing["created_on"]

                listings_list.append({
                    "sellerId": sellerId,
                    "listingId": listingId,
                    "title": title,
                    "price": price,
                    "location": safe_address,
                    "status": status,
                    "listedAt": listedAt,
                    "lastUpdatedAt": listedAt,  # will be updated once alg returns last updated time
                })

            return make_ok_response(body=listings_list)

        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()

    return make_internal_error_response()


def get_recommendations(http, auth_token):
    creds = resolve_credentials(auth_token)
    if not creds:
        return make_unauthorized_response()

    result = http.request(
        "GET", f"http://serber.ddns.net:32500/recommendations?userId={creds}")

    if result.status == 200:
        try:
            data = result.json()
            listings_list = []

            for listing in data:
                sellerId = listing["seller_id"]
                listingId = listing["listing_id"]
                title = listing["title"]
                price = listing["price"]
                full_address = listing["address"]
                safe_address = address_to_postal_code(full_address)
                status = listing["status"]
                listedAt = listing["created_on"]

                listings_list.append({
                    "sellerId": sellerId,
                    "listingId": listingId,
                    "title": title,
                    "price": price,
                    "location": safe_address,
                    "status": status,
                    "listedAt": listedAt,
                    "lastUpdatedAt": listedAt,  # will be updated once alg returns last updated time
                })

            return make_ok_response(body=listings_list)

        except json.decoder.JSONDecodeError:
            return make_not_found_response()
        except Exception as e:
            make_internal_error_response()
    elif result.status == 404:
        return make_not_found_response("Listing not found")

    return make_internal_error_response()


def request_account(email, callback):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return make_invalid_request_response()

    encoded = jwt.encode({
        "eml": email,
        "exp": int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)).timestamp())
    }, JWT_SECRET, algorithm="HS256")
    print("CREATE ACCOUNT REQUEST:")
    print(f"\t{callback}{encoded}")
    # TODO: send email
    return make_ok_response()


def verify_account(http, token, username, password, address):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = decoded["eml"]
        if not re.match(r"^[a-zA-Z0-9_@]{6,20}$", username):
            print("invalid username format")
            return make_invalid_request_response("Username does not meet the requirements")
        if not re.match(r"^[^@]+@uvic\.ca$", email):
            print("invalid email format")
            return make_invalid_request_response("Email does not meet the requirements")
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$", password):
            print("invalid password format")
            return make_invalid_request_response("Password does not meet the requirements")

        salt = hashlib.sha256(username.encode("ascii"),
                              usedforsecurity=True).hexdigest()
        hashed_password = hashlib.sha256(
            f"{password}{salt}".encode("ascii"), usedforsecurity=True).hexdigest()

        parsed_address = parse_address(address)

        if parsed_address is None:
            print(f"failed to parse address {address}")
            return make_invalid_request_response("Invalid address")

        full_address = parsed_address.full_address

        geocode_result = address_to_latlng(http, full_address)
        if geocode_result is None:
            print(f"failed to geocode address {address}")
            return make_internal_error_response()

        lat, lng = geocode_result
        body = {
            "email": email,
            "username": username,
            "password": hashed_password,
            "address": full_address,
            "location": {
                "lat": lat,
                "lng": lng
            },
            "join_date": datetime.datetime.now(datetime.UTC).isoformat()
        }
        result = execute_data_post(http, "/make_user", body=body)
        if result.status == 200:
            b = result.json()
            user_id = b["user_id"]
            exp = datetime.datetime.now(
                datetime.UTC) + datetime.timedelta(hours=3)
            token = jwt.encode({
                "exp": int(exp.timestamp()),
                "uid": user_id,
            }, JWT_SECRET)
            return make_created_response(body={
                "userId": user_id
            }, auth={
                "jwt": token,
                "exp": exp,
            })
        elif result.status == 400:
            return make_invalid_request_response("Account already exists")
        else:
            print(f"failed to call data layer, status={result.status}")
            return make_internal_error_response()
    except Exception as e:
        print("decoding failed")
        print(e)

    return make_internal_error_response()


def request_reset(email, callback):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return make_invalid_request_response()

    encoded = jwt.encode({
        "eml": email,
        "exp": int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)).timestamp())
    }, JWT_SECRET, algorithm="HS256")
    print("CREATE ACCOUNT REQUEST:")
    print(f"\t{callback}{encoded}")
    # TODO: send email
    return make_ok_response()


def verify_reset(http, token, password):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = decoded["eml"]
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}$", password):
            return make_invalid_request_response()

        print(f"email: {email}")
        res = execute_data_get(http, f"/get_user_by_email?eml={email}")
        print(res.status)
        if res.status != 200:
            print("could not get user by email")
            return make_internal_error_response()

        res_json = res.json()
        user_id = res_json["user_id"]
        username = res_json["username"]

        salt = hashlib.sha256(username.encode("ascii"),
                              usedforsecurity=True).hexdigest()
        hashed_password = hashlib.sha256(
            f"{password}{salt}".encode("ascii"), usedforsecurity=True).hexdigest()

        execute_data_post(http, "/update_user_password", body={
            "user_id": user_id,
            "password": hashed_password,
        })
        return make_ok_response()
    except Exception as e:
        print("decoding failed")
        print(e)

    return make_internal_error_response()


def login(http, username, password):
    print(f"username: {username} password: {password}")
    res = execute_data_get(http, f"/get_user_info_for_login?usr={username}")

    if res.status != 200:
        print("username lookup failed")
        return make_invalid_request_response()

    res_json = res.json()

    user_id = res_json["user_id"]
    existing_password = res_json["password"]

    salt = hashlib.sha256(username.encode("ascii"),
                          usedforsecurity=True).hexdigest()
    hashed_password = hashlib.sha256(
        f"{password}{salt}".encode("ascii"), usedforsecurity=True).hexdigest()

    print(f"hashed: {hashed_password}")
    print(f"existing: {existing_password}")
    if hashed_password == existing_password:
        # generate token
        exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=3)
        token = jwt.encode({
            "exp": int(exp.timestamp()),
            "uid": user_id,
        }, JWT_SECRET)
        return make_ok_response(auth={
            "jwt": token,
            "exp": exp,  # must pass the expiration time as a datetime as well so that flask can set the expiration field on the cookie
        })

    print("invalid password")
    return make_invalid_request_response()


def not_implemented():
    return {
        "statusCode": 501,
        "body": json.dumps({
            "message": "NOT IMPLEMENTED"
        })
    }
