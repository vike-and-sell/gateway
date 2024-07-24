from .common import make_response
from flask import Blueprint, Response, request
import gateway
import smtplib
import os
import urllib3
http = urllib3.PoolManager()


auth_bp = Blueprint('auth', __name__)

SMTP_USERNAME = os.environ["SMTP_USERNAME"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = int(os.environ["SMTP_PORT"])


@auth_bp.post('/request_account')
def request_account():
    body = request.get_json()
    email = body["email"]
    callback = body["callback"]
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        result = gateway.request_account(server, email, callback)
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


@auth_bp.delete('/login')
def logout():
    result = gateway.logout()
    return make_response(result)


@auth_bp.post('/request_reset')
def request_reset():
    body = request.get_json()
    email = body["email"]
    callback = body["callback"]
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        result = gateway.request_reset(server, email, callback)
        return make_response(result)


@auth_bp.post('/verify_reset')
def verify_reset():
    body = request.get_json()
    token = body["jwt"]
    password = body["password"]
    print(f"jwt: {token} password: {password}")
    result = gateway.verify_reset(http, token, password)
    return make_response(result)
