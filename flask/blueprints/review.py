from flask import Blueprint, Response, request, make_response
import gateway
import urllib3

review_bp = Blueprint('review', __name__)
http = urllib3.PoolManager()

@review_bp.get('/<int:listing_id>')
def get_review(listing_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_reviews_by_listing_id(http, auth_token, listing_id)
    return make_response(result)

@review_bp.post('/<int:listing_id>')
def create_review(listing_id):
    review = request.json
    auth_token = request.cookies.get("Authorization")
    result = gateway.post_review_by_listing_id(http, auth_token, listing_id, review)
    return make_response(result)
