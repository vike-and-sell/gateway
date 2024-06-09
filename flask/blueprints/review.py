from flask import Blueprint, Response
import gateway

review_bp = Blueprint('review', __name__)

@review_bp.get('/<int:listing_id>')
def get_review(listing_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@review_bp.post('/<int:listing_id>')
def create_review(listing_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")
