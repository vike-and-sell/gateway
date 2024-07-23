from flask import Blueprint, Response, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

listings_bp = Blueprint('listings', __name__)


@listings_bp.post('/')
def create_listing():
    auth_token = request.cookies.get("Authorization")
    title = request.json.get('title')
    price = request.json.get('price')
    address = request.json.get('address')
    result = gateway.create_listing(http, auth_token, title, price, address)
    return make_response(result)


@listings_bp.patch('/<int:listing_id>')
def patch_listing(listing_id):
    auth_token = request.cookies.get("Authorization")
    title = request.json.get('title')
    price = request.json.get('price')
    address = request.json.get('address')
    status = request.json.get('status')
    buyer_user_name = request.json.get('buyerUsername')
    result = gateway.update_listing(
        http, auth_token, listing_id, title, price, address, status, buyer_user_name)
    return make_response(result)


@listings_bp.delete('/<int:listing_id>')
def delete_listing(listing_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.delete_listing(http, auth_token, listing_id)
    return make_response(result)


@listings_bp.get('/')
def get_listings():
    auth_token = request.cookies.get("Authorization")
    max_price = request.args.get('maxPrice')
    min_price = request.args.get('minPrice')
    status = request.args.get('status')
    sort_by = request.args.get('sortBy')
    is_descending = request.args.get('isDescending')

    if is_descending == "true":
        is_descending = True
    else:
        is_descending = False
    
    if min_price:
        min_price = float(min_price)
    if max_price:
        max_price = float(max_price)
    result = gateway.get_sorted_listings(http, auth_token, 
        max_price, min_price, status, sort_by, is_descending)
    return make_response(result)


@listings_bp.get('/<int:listing_id>')
def get_listing(listing_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_listing_by_id(http, auth_token, listing_id)
    return make_response(result)


@listings_bp.get('/me')
def my_listings():
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_my_listings(http, auth_token)
    return make_response(result)
