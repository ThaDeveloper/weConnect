import os
import sys
import inspect
from flask import Flask, request, jsonify, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from src.v2.models import User
from src.utils import validate_user

auth = Blueprint('user', __name__)
tokens = {}


def token_required(f):
    """All endoints that need log in will be wrapped by this decorator"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'Message': 'You need to log in'}), 401

        try:
            data = jwt.decode(token, os.getenv('SECRET'))
            if data['public_id'] in tokens:
                current_user = User.query.filter_by(
                    public_id=data['public_id']).first()
            else:
                return jsonify({"Message": "Token expired:Login again"}), 401
        except BaseException:
            return jsonify({'Message': 'Invalid request!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth.route('/register', methods=['POST'])
def create_user():
    """Receive user input as json object"""
    data = request.get_json()
    if validate_user(data):
        return validate_user(data)
    new_user = User(username=data['username'], password=data['password'])
    # check for duplicates before creating the new user
    duplicate = User.query.filter_by(username=new_user.username).first()
    if not duplicate:
        new_user.add()
        return jsonify({"Message": "User registered successfully"}), 201
    return jsonify({"Message": "User already exist"}), 400


@auth.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'Message': "Cannot perform that action"}), 401
    users = User.query.all()
    if users:
        return jsonify({
            'Users': [
                {
                    'id': user.id,
                    'username': user.username,
                    'password': user.password,
                    'admin': user.admin,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                } for user in users
            ]
        }), 200
    return jsonify({"Message": "No available users"}), 400

@auth.route('/users/<id>', methods=['GET'])
@token_required
def get_user(current_user, id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'Message': 'User not found'}), 404
    if not current_user.admin or not current_user.id == id:
        return jsonify({'Message': "Cannot perform that action"}), 401
    return jsonify({
        'Users': [
            {
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'admin': user.admin,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
        ]
    }), 200


@auth.route('/users/<id>', methods=['PUT'])
@token_required
def promote_user(current_user, id):
    if not current_user.admin:
        return jsonify({'Message': "Cannot perform that action"}), 401
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'Message': 'User not found'})
    user.admin = True
    user.add()
    return jsonify({'Message': 'User is now an admin'}), 200


@auth.route('/users/<id>', methods=['DELETE'])
@token_required
def remove_user(current_user, id):
    if not current_user.admin:
        return jsonify({'Message': "Cannot perform that action"}), 401
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'Message': 'User not found'})
    user.delete()
    return jsonify({'Message': 'User deleted successfully'}), 200


@auth.route('/login', methods=['POST'])
def login():
    """Log in and generate token"""
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"Message": "login required!"}), 401
    user = User.query.filter_by(username=auth['username']).first()
    if not user:
        return jsonify({"Message": "Username not found!"}), 401
    if check_password_hash(user.password, auth['password']):
        session['loggedin'] = True
        session['username'] = auth['username']
        token = jwt.encode({'public_id': user.public_id,
                            'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=30)},
                           os.getenv('SECRET'))
        tokens[user.public_id] = token
        # user_object.u_token[user['username']] = token
        return jsonify({"token": token.decode('UTF-8')}), 200
    return jsonify({"Message": "login invalid!"}), 401


@auth.route('/logout', methods=['DELETE'])
@token_required
def logout(current_user):
    """Destroy user session"""
    if session and session['loggedin']:
        session.clear()
        return jsonify({"Message": "logged out"}), 200
    return jsonify({"Message": "Already logged out"}), 400


@auth.route('/reset-password', methods=['PUT'])
@token_required
def reset_password(current_user):
    """
    User must be logged in to update password
    """
    data = request.get_json()
    password_hash = generate_password_hash(data['password'], method='sha256')
    user = User.query.filter_by(username=data['username']).first()
    user.password = password_hash
    user.add()
    return jsonify({"Message": "Password updated"}), 202


@auth.route('/users/<id>/businesses', methods=['GET'])
def read_user_businesses(id):
    """Get all businesses owned by a particular user"""
    user = User.query.get(id)
    if user:
        return jsonify(
            [
                {
                    'id': business.id,
                    'name': business.name,
                    'description': business.description,
                    'location': business.location,
                    'category': business.category,
                    'owner': business.owner.username,
                    'created_at': business.created_at,
                    'updated_at': business.updated_at
                } for business in user.businesses
            ]
        ), 200

    return jsonify({'warning': 'User has zero businesses'}), 400