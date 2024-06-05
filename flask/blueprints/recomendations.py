from flask import Blueprint, jsonify

recomendations_bp = Blueprint('recomendations', __name__)

@recomendations_bp.get('/')
def get_recomendations():
    return {}

@recomendations_bp.post('/<int:listing_id>/ignore')
def ignore_recomendations(listing_id):
    return {}
