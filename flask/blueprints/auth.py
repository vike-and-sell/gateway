from flask import Blueprint, Response
import gateway

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/request_account')
def request_account():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@auth_bp.post('/verify_account')
def verify_account():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@auth_bp.post('/login')
def login():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json") 

@auth_bp.post('/request_reset')
def request_reset():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json") 

@auth_bp.post('/verify_reset')
def verify_reset():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json") 