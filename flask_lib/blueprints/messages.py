from flask import Blueprint, jsonify

messages_bp = Blueprint('messages', __name__)

@messages_bp.get('/updates')
def get_updates(messages_id):
    return {}

@messages_bp.get('/<int:chat_id>')
def get_messages(chat_id):
    return {}