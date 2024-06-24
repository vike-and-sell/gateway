from flask import Blueprint, Response, make_response
import gateway

search_bp = Blueprint('search', __name__)

@search_bp.get('/')
def get_search(q = None):
    result = gateway.not_implemented()
    return make_response(result)
