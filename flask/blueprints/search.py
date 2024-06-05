from flask import Blueprint, jsonify

search_bp = Blueprint('search', __name__)

@search_bp.get('/')
def get_search(q = None):
    return {}
