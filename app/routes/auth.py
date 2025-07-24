from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(key in data for key in ('username', 'email', 'password')):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter((User.user_name == data['username']) | (User.email == data['email'])).first():
        return jsonify({"error": "User already exists"}), 400
    
    user = User(user_name=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not all(key in data for key in ('username', 'password')):
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(user_name=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    return jsonify(access_token=access_token), 200