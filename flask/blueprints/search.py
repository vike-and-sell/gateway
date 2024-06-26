from flask import Blueprint, Response, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

search_bp = Blueprint('search', __name__)


@search_bp.get('/')
def get_search():
    q = request.args.get("query")
    auth = request.cookies.get("Authorization")
    result = gateway.get_search(http, auth, q)
    return make_response(result)
