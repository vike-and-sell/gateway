from flask import Blueprint, Response
import gateway
from .common import make_response

search_bp = Blueprint('search', __name__)


@search_bp.get('/')
def get_search(q=None):
    result = gateway.not_implemented()
    return make_response(result)
