from flask import Blueprint, jsonify
import gateway

users_bp = Blueprint('user', __name__)

@users_bp.patch('/<int:user_id>')
def patch_user(user_id):
    return {}

@users_bp.get('/me')
def my_user():
    return {}

@users_bp.get('/<int:user_id>')
def get_user(user_id):
    return {}

@users_bp.get('/<int:user_id>/searches')
def searches_by_user(user_id):
    return {}