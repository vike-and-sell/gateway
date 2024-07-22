from flask import Blueprint, Response, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

charity_bp = Blueprint('charity', __name__)

@charity_bp.get('/')
def get_charities():
    auth_token = request.cookies.get("Authorization")

    result = gateway.get_charities(http, auth_token)
    return make_response(result)

