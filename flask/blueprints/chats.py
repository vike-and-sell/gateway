from flask import Blueprint, Response, request
import gateway
from .common import make_response
import urllib3

http = urllib3.PoolManager()

chats_bp = Blueprint('chats', __name__)


@chats_bp.get('/')
def my_chats():
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_chats(http, auth_token)
    return make_response(result)


@chats_bp.get('/<int:chat_id>')
def get_chats(chat_id):
    auth_token = request.cookies.get("Authorization")
    result = gateway.get_chat_preview(http, auth_token, chat_id)
    return make_response(result)
