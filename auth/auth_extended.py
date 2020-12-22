from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
    get_jwt_identity
)
from flask import request, jsonify
from werkzeug.security import safe_str_cmp
import sys

from api.models import User
from . import auth
from http_status import HttpStatus
from database.db_manager import DbManager

DB = DbManager()

@auth.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request'}), HttpStatus.bad_request_400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({'msg': 'Missing email parameter'}), HttpStatus.bad_request_400
    if not password:
        return jsonify({'msg': 'Missing password parameter'}), HttpStatus.bad_request_400

    user = User(*DB.get_user(email))
    if user and safe_str_cmp(user.password, password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token
            }), HttpStatus.accepted_202

@auth.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request'}), HttpStatus.bad_request_400
    data = request.get_json()
    if 'email' not in data:
        return jsonify({'msg': 'Missing email parameter'}), HttpStatus.bad_request_400
    if 'password' not in data:
        return jsonify({'msg': 'Missing password parameter'}), HttpStatus.bad_request_400
    if 'username' not in data:
        return jsonify({'msg': 'Missing username parameter'}), HttpStatus.bad_request_400

    user = User(data)
    user_id = DB.add_user(user)
    if user_id:
        user.set_id(user_id())
        access_token = create_access_token(identity=user.email, fresh=True)
        refresh_token = create_refresh_token(user.email)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), HttpStatus.created_201
    else:
        return jsonify({'msg': 'User already exists'}), HttpStatus.conflict_409


@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    return jsonify({'access_token': new_token}), HttpStatus.created_201
