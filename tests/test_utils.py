import jwt
import os

import gateway

DATA_URL = os.environ["DATA_URL"]
DATA_API_KEY = os.environ["DATA_API_KEY"]
JWT_SECRET = os.environ["JWT_SECRET_KEY"]
MAPS_API_KEY = os.environ["MAPS_API_KEY"]


def sign_jwt_for_test(body) -> str:
    return jwt.encode(body, JWT_SECRET, algorithm="HS256")


def wrong_jwt_for_test(body) -> str:
    return jwt.encode(body, f"{JWT_SECRET}asdf", algorithm="HS256")


def test_auth_helper():
    signed = sign_jwt_for_test({
        "uid": 5678
    })
    assert gateway.resolve_credentials(signed) == 5678
    assert gateway.resolve_credentials("123") == None
