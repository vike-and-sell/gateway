from flask import Blueprint, Response, request
import gateway
from shared import make_response
import urllib3

http = urllib3.PoolManager()
auth_token = request.cookies.get("Authorization")

chats_bp = Blueprint('chats', __name__)

@chats_bp.get('/')
def my_chats():
    result = gateway.get_chats(http, auth_token)
    return make_response(result)

@chats_bp.get('/<int:chats_id>')
def get_chats(chats_id):
    result = gateway.get_messages(http, auth_token, chats_id)
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")