from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models import create_user
from db import db

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    existing_user = db.users.find_one({'email': data['email']})
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = create_user(data['username'], data['email'], hashed_password)
    db.users.insert_one(new_user)
    
    return jsonify({'message': 'Account created successfully!'}), 201

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = db.users.find_one({'email': data['email']})
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not bcrypt.check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=str(user['_id']))
    
    return jsonify({'token': access_token}), 200