import os
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

auth = Blueprint('auth', __name__)

jwt_username = os.getenv('JWT_USERNAME')
jwt_password = os.getenv('JWT_PASSWORD')

@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != jwt_username or password != jwt_password:
        return jsonify({'login': False}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)