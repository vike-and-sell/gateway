from flask import Blueprint, Response, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

search_bp = Blueprint('search', __name__)


@search_bp.get('/')
def get_search():
    q = request.args.get("search")
    auth = request.cookies.get("Authorization")
    max_price = request.args.get('maxPrice')
    min_price = request.args.get('minPrice')
    status = request.args.get('status')
    sort_by = request.args.get('sortBy')
    is_descending = request.args.get('isDescending')

    if is_descending == "true":
        is_descending = True
    else:
        is_descending = False
    
    if min_price:
        min_price = float(min_price)
    if max_price:
        max_price = float(max_price)
    result = gateway.get_search(http, auth, q, min_price, max_price, status, sort_by, is_descending)
    return make_response(result)
