from flask import Blueprint, request, jsonify
from backend.models import User, Tenant
from backend.extensions import db
# from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register(tenant):
    data = request.json
    # Logic to register user for 'tenant'
    return jsonify({"message": "User registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login(tenant):
    data = request.json
    # Logic to login
    return jsonify({"token": "fake-jwt-token", "user_id": 1}), 200
