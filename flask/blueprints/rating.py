from flask import Blueprint, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

rating_bp = Blueprint('rating', __name__)


@rating_bp.get('/<int:listing_id>')
def get_rating(listing_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_ratings_by_listing_id(http, auth_token, listing_id)
    return make_response(result)


@rating_bp.post('/<int:listing_id>')
def create_rating(listing_id):
    auth_token = request.cookies.get("Authorization")
    rating = request.json.get('ratingValue')
    result = gateway.post_rating_by_listing_id(
        http, auth_token, listing_id, rating)
    return make_response(result)
