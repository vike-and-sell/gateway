from flask import Blueprint, Response, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

listings_bp = Blueprint('listings', __name__)


@listings_bp.post('/')
def create_listing():
    auth_token = request.cookies.get("Authorization")
    result = gateway.create_listing(http, auth_token, request.json)
    return make_response(result)


@listings_bp.patch('/<int:listing_id>')
def patch_listing(listing_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.update_listing(http, auth_token, listing_id, request.json)
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

    params = ""
    if max_price is not None:
        params += f"maxPrice={max_price}&"
    if min_price is not None:
        params += f"minPrice={min_price}&"
    if status is not None:
        params += f"status={status}&"
    if sort_by is not None:
        params += f"sortBy={sort_by}&"
    if is_descending is not None:
        params += f"isDescending={is_descending}"

    result = gateway.get_sorted_listings(http, auth_token, params)
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
