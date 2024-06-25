from flask import Blueprint, Response, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

messages_bp = Blueprint('messages', __name__)


@messages_bp.post('/<int:chat_id>')
def get_updates(chat_id):
    auth_token = request.cookies.get("Authorization")
    body = request.get_json()
    content = body["content"]
    result = gateway.write_message(http, auth_token, chat_id, content)
    return make_response(result)


@messages_bp.get('/<int:chat_id>')
def get_messages(chat_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_messages(http, auth_token, chat_id)
    return make_response(result)
