from flask import Blueprint, jsonify

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.get('/')
def get_recommendations():
    return {}

@recommendations_bp.post('/<int:listing_id>/ignore')
def ignore_recommendations(listing_id):
    return {}
