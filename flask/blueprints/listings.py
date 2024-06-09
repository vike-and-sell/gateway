from flask import Blueprint, Response
import gateway

listings_bp = Blueprint('listings', __name__)

@listings_bp.post('/')
def create_listing():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@listings_bp.patch('/<int:listing_id>')
def patch_listing(listing_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@listings_bp.delete('/<int:listing_id>')
def delete_listing(listing_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@listings_bp.get('/')
def get_listings():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@listings_bp.get('/<int:listing_id>')
def get_listing(listing_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@listings_bp.get('/me')
def my_listings():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")
