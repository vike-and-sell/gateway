from flask import Blueprint, Response
import gateway

chats_bp = Blueprint('chats', __name__)

@chats_bp.get('/')
def my_chats():
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@chats_bp.get('/<int:chats_id>')
def get_chats(chats_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")