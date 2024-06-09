from flask import Blueprint, Response
import gateway

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.get('/')
def get_recommendations():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@recommendations_bp.post('/<int:listing_id>/ignore')
def ignore_recommendations(listing_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")
