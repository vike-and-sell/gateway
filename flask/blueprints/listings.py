from flask import Blueprint, jsonify
import gateway

listings_bp = Blueprint('listings', __name__)

@listings_bp.post('/')
def create_listing():
    return {}

@listings_bp.patch('/<int:listing_id>')
def patch_listing(listing_id):
    return {}

@listings_bp.delete('/<int:listing_id>')
def delete_listing(listing_id):
    return {}

@listings_bp.get('/')
def get_listings():
    return {}

@listings_bp.get('/<int:listing_id>')
def get_listing(listing_id):
    return {}

@listings_bp.get('/me')
def my_listings():
    return {}
