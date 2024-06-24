from flask import Blueprint, Response, request
import gateway
from shared import make_response
import urllib3

http = urllib3.PoolManager()
auth_token = request.cookies.get("Authorization")

listings_bp = Blueprint('listings', __name__)

@listings_bp.post('/')
def create_listing():
    result = gateway.create_listing(http, auth_token, request.json)
    return make_response(result)

@listings_bp.patch('/<int:listing_id>')
def patch_listing(listing_id):
    result = gateway.update_listing_by_id(http, auth_token, listing_id, request.json)
    return make_response(result)

@listings_bp.delete('/<int:listing_id>')
def delete_listing(listing_id):
    result = gateway.delete_listing_by_id(http, auth_token, listing_id)
    return make_response(result)

@listings_bp.get('/')
def get_listings():
    result = gateway.get_sorted_listings(http, auth_token)
    return make_response(result)

@listings_bp.get('/<int:listing_id>')
def get_listing(listing_id):
    result = gateway.get_listing_by_id(http, auth_token, listing_id)
    return make_response(result)

@listings_bp.get('/me')
def my_listings():
    result = gateway.get_my_listings(http, auth_token)
    return make_response(result)
