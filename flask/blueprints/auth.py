from .common import make_response
from flask import Blueprint, Response, request
import gateway
import urllib3
http = urllib3.PoolManager()


auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/request_account')
def request_account():
    body = request.get_json()
    email = body["email"]
    callback = body["callback"]
    result = gateway.request_account(email, callback)
    return make_response(result)


@auth_bp.post('/verify_account')
def verify_account():
    body = request.get_json()
    jwt = body["jwt"]
    username = body["username"]
    password = body["password"]
    location = body["location"]
    result = gateway.verify_account(http, jwt, username, password, location)
    return make_response(result)


@auth_bp.post('/login')
def login():
    body = request.get_json()
    username = body["username"]
    password = body["password"]
    result = gateway.login(http, username, password)
    return make_response(result)


@auth_bp.post('/request_reset')
def request_reset():
    result = gateway.not_implemented()
    return make_response(result)


@auth_bp.post('/verify_reset')
def verify_reset():
    result = gateway.not_implemented()
    return make_response(result)
