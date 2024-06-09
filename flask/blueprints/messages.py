from flask import Blueprint, Response
import gateway

messages_bp = Blueprint('messages', __name__)

@messages_bp.get('/updates')
def get_updates(messages_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")

@messages_bp.get('/<int:chat_id>')
def get_messages(chat_id):
    result = gateway.not_implemented()
    return Response(result["body"], status=result["statusCode"], mimetype="application/json")