from flask import Blueprint, Response, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

users_bp = Blueprint('user', __name__)


@users_bp.patch('/me')
def patch_user():
    auth_token = request.cookies.get("Authorization")
    result = gateway.update_user(
        http, auth_token, request.json.get("location"), request.json.get('seeCharity'))
    return make_response(result)


@users_bp.get('/me')
def my_user():
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_user_by_auth_token(http, auth_token)
    return make_response(result)


@users_bp.get('/<int:user_id>')
def get_user(user_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_user_by_id(http, auth_token, user_id)
    return make_response(result)


@users_bp.get('/me/searches')
def searches_by_user():
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_search_history(http, auth_token)
    return make_response(result)
