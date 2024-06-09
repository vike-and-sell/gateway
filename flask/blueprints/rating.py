from flask import Blueprint, Response
import gateway

rating_bp = Blueprint('rating', __name__)

@rating_bp.get('/<int:listing_id>')
def get_rating(listing_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@rating_bp.post('/<int:listing_id>')
def create_rating(listing_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")
