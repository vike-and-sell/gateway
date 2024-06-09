from flask import Blueprint, Response
import gateway

search_bp = Blueprint('search', __name__)

@search_bp.get('/')
def get_search(q = None):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")
