from flask import Blueprint, jsonify
import gateway

chats_bp = Blueprint('chats', __name__)

@chats_bp.get('/')
def my_chats():
    return {}

@chats_bp.get('/<int:chats_id>')
def get_chats(chats_id):
    return {}