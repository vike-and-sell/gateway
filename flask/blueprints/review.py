from flask import Blueprint, jsonify

review_bp = Blueprint('review', __name__)

@review_bp.get('/<int:listing_id>')
def get_review(listing_id):
    return {}

@review_bp.post('/<int:listing_id>')
def create_review(listing_id):
    return {}
