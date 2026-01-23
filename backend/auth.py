"""
Authentication Blueprint
Handles user signup, login, and session management
"""
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import get_users_collection
from backend.auth_utils import generate_token, verify_token, require_auth
from datetime import datetime
from bson import ObjectId
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Password validation (minimum 6 characters)
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        users_collection = get_users_collection()
        
        # Check if user already exists
        if users_collection.find_one({'email': email}):
            return jsonify({'error': 'Email already registered'}), 409
        
        # Hash password and create user
        hashed_password = generate_password_hash(password)
        user_data = {
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = users_collection.insert_one(user_data)
        user_id = str(result.inserted_id)
        
        # Generate JWT token
        token = generate_token(user_id, email)
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': user_id,
                'email': email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Signup failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        users_collection = get_users_collection()
        user = users_collection.find_one({'email': email})
        
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate JWT token
        user_id = str(user['_id'])
        token = generate_token(user_id, email)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user_id,
                'email': email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/verify', methods=['GET'])
@require_auth
def verify():
    """Verify token and get user info"""
    try:
        user_id = request.user_id
        users_collection = get_users_collection()
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': str(user['_id']),
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Verification failed: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout endpoint (client-side token removal)"""
    return jsonify({'message': 'Logged out successfully'}), 200
