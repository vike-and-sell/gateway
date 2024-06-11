import os
import json
import jwt.exceptions
import jwt.utils
import urllib3
import jwt

DATA_URL = os.environ["DATA_URL"]
DATA_API_KEY = os.environ["DATA_API_KEY"]
JWT_SECRET = os.environ["JWT_SECRET_KEY"]


def resolve_credentials(auth_token: str):
    try:
        return jwt.decode(auth_token, JWT_SECRET, algorithms="HS256")
    except Exception:
        return None


def make_ok_response(body: dict, headers: dict = None):
    if headers:
        return {
            "statusCode": 200,
            "body": json.dumps(body),
            "headers": headers,
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps(body)
        }


def make_unauthorized_response():
    return {
        "statusCode": 401,
    }


def make_not_found_response():
    return {
        "statusCode": 404,
    }


def make_internal_error_response():
    return {
        "statusCode": 500,
    }


def execute_data_request(http: urllib3.PoolManager, path, method, body):
    headers = {
        "X-Api-Key": DATA_API_KEY,
    }
    print(f"data url: {DATA_URL}")
    print(f"path: {path}")
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
            print(result.data)
            return make_ok_response(result.json())
        except json.decoder.JSONDecodeError:
            return make_not_found_response()

    return make_internal_error_response()


def not_implemented():
    return {
        "statusCode": 501,
        "body": json.dumps({
            "message": "NOT IMPLEMENTED"
        })
    }
