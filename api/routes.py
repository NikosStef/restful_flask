from flask import abort, jsonify, request, url_for, Response
from flask_jwt import jwt_required
import sys

from database.db_manager import DbManager
from http_status import HttpStatus
from . import api_bp
from .models import User, Note
from .errors import bad_request

DB = DbManager()

@api_bp.route('/user/<int:id>', methods=['GET'])
@jwt_required
def get_user(id):
    user = DB.get_user_by_id(id)
    if user is None:
        abort(HttpStatus.not_found_404.value)
    response = User.from_tuple(user)
    return response.to_dict()
'''
'''
@api_bp.route('/user', methods=['POST'])
def post_user():

    data = request.get_json() or {}
    if 'email' not in data:
        return bad_request('must include email')

    user = User.from_dict(data)
    user.set_id(*DB.add_user(user))
    print(user.to_dict(), file=sys.stderr)

    response = jsonify(user.to_dict())
    response.status_code = HttpStatus.created_201.value
    response.headers['Location'] = url_for('api.get_note', id=user.id)
    return response


@api_bp.route('/note/<int:id>', methods=['GET'])
def get_note(id):
    note = DB.get_note(id)
    if note is None:
        abort(HttpStatus.not_found_404.value)
    response = Note.from_tuple(note)
    return response.to_dict()

@api_bp.route('/note', methods=['POST'])
@jwt_required()
def post_note():
    data = request.get_json() or {}
    print(data, file=sys.stderr)
    if 'context' not in data or 'ownerEmail' not in data:
        return bad_request('must include context and owner email')
    note = Note.from_dict(data)
    print(note.to_dict(), file=sys.stderr)
    note.set_id(*DB.add_note(note))
    print(note.to_dict(), file=sys.stderr)

    response = jsonify(note.to_dict())
    response.status_code = HttpStatus.created_201.value
    response.headers['Location'] = url_for('api.get_note', id=note.id)
    return response
