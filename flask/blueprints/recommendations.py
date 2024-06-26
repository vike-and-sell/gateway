from flask import Blueprint, Response, request
from .common import make_response
import gateway
import urllib3

http = urllib3.PoolManager()

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.get('/')
def get_recommendations():
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_recommendations(http, auth_token)
    return make_response(result) 

@recommendations_bp.post('/<int:listing_id>/ignore')
def ignore_recommendations(listing_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.not_implemented()
    return make_response(result)