from flask import Blueprint, jsonify
import gateway

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/request_account')
def request_account():
    return {}

@auth_bp.post('/verify_account')
def verify_account():
    return {} 

@auth_bp.post('/login')
def login():
    return {} 

@auth_bp.post('/request_reset')
def request_reset():
    return {} 

@auth_bp.post('/verify_reset')
def verify_reset():
    return {} 