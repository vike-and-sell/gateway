from flask import Blueprint, Response, request
import gateway
from shared import make_response
import urllib3

http = urllib3.PoolManager()
auth_token = request.cookies.get("Authorization")

messages_bp = Blueprint('messages', __name__)

@messages_bp.get('/updates')
def get_updates(messages_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@messages_bp.get('/<int:chat_id>')
def get_messages(chat_id):
    result = gateway.get_messages(http, auth_token, chat_id)
    return make_response(result)