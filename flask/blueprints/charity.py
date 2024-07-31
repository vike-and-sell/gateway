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

@charity_bp.post('/')
def add_charity():
    auth_token = request.cookies.get("Authorization")
    key = request.json.get('key')
    name = request.json.get('name')
    status = request.json.get('status')
    logo_url = request.json.get('logoUrl')
    start_date = request.json.get('startDate')
    end_date = request.json.get('endDate')

    result = gateway.add_charity(http, auth_token, key, name, status, logo_url, start_date, end_date)
    return make_response(result)