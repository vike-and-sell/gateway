from flask import Blueprint, jsonify
import gateway

rating_bp = Blueprint('rating', __name__)

@rating_bp.get('/<int:listing_id>')
def get_rating(listing_id):
    return {}

@rating_bp.post('/<int:listing_id>')
def create_rating(listing_id):
    return {}
