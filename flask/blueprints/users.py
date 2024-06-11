from flask import Blueprint, Response, request
import gateway

import urllib3
http = urllib3.PoolManager()

users_bp = Blueprint('user', __name__)


def make_response(result):
    return Response(result.get("body"), status=result.get("statusCode"), mimetype="application/json")


@users_bp.patch('/<int:user_id>')
def patch_user(user_id):
    result = gateway.not_implemented()
    return make_response(result)


@users_bp.get('/me')
def my_user():
    result = gateway.not_implemented()
    return make_response(result)


@users_bp.get('/<int:user_id>')
def get_user(user_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_user_by_id(http, auth_token, user_id)
    return make_response(result)


@users_bp.get('/<int:user_id>/searches')
def searches_by_user(user_id):
    result = gateway.not_implemented()
    return make_response(result)
