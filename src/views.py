from flask import Flask, request, jsonify, make_response,session, Blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
import jwt
import datetime
from functools import wraps
import os
import sys
import inspect
"""python can't perform relaive import but pytest hence the need for absolute import"""
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.models import User, Business
from src.config import app_config

app = Flask(__name__)


"""Instances of User and Business class"""
user_object = User()
business_object = Business()

app.config['SECRET_KEY'] = 'doordonotthereisnotry'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'Message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # current_user = find_user_by_username(data['username'])
            if data['username'] in user_object.u_token:
                current_user = user_object.users[data['username']]
            else:
                return jsonify({"Message": "Token expired"})
        except:
            return jsonify({'Message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/v1/auth/register',  methods=['POST'])
def create_user():
    """receive user input as json object"""
    data = request.get_json()
    password_hash =  generate_password_hash(data['password'], method='sha256')
    
    if data['username'] in user_object.users:
        return jsonify({'Message': "User already exists"}), 400
    if data['username'] == "" or data['password'] == "":
            return jsonify({'Message': 
                "Username and Password is required"}),400

    data = user_object.create_user(data['username'], password_hash)
    return jsonify({"Message": "User registered successfully"}), 201

  
@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"Message": "login required!"}), 401

    if auth['username'] not in user_object.users.keys():
       
        return jsonify({"Message": "Username not found!"}), 401

    user = user_object.users[auth['username']]
    if check_password_hash(user['password'], auth['password']):
        token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow() + 
            datetime.timedelta(minutes=20)}, app.config['SECRET_KEY'])
        user_object.u_token[user['username']] = token
        return jsonify({"token": token.decode('UTF-8')}), 200

    return jsonify({"Message": "login invalid!"}), 401


@app.route('/api/v1/auth/logout', methods = ['DELETE'])
@token_required
def logout(current_user):
    session.clear()
    return jsonify({"Message": "Logged out"}), 202


@app.route('/api/v1/auth/reset-password', methods=['GET0','PUT'])
@token_required
def reset_password(current_user):
    """
    User must be logged in to update password
    """
    data = request.get_json()
    password_hash = generate_password_hash(data['password'], method='sha256')
    usr = user_object.users[current_user["username"]]
    usr.update({"password": password_hash})
    return jsonify({"Message": "password updated"}), 202


@app.route('/api/v1/auth/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    return jsonify({"users": user_object.users}), 200


@app.route('/api/v1/businesses', methods=['POST'])
@token_required
def create_business(current_user):
    data = request.get_json()
    if not data or not data['name']:
        return jsonify({"Message": "Name is required!"}), 400

    if data['name'] in business_object.businesses:
        return jsonify({"Message": "Name already exists!"}), 400
    # add business
    user_id = current_user['username']
    res=business_object.register_business(data['name'], data['description'], data['location'],
                                  data['category'], user_id)
    return jsonify({"Message": res}), 201


@app.route('/api/v1/businesses/<string:business_id>', methods=['GET'])
def get_one_business(business_id):
    """Return a single business"""
    response = business_object.find_business_by_id(business_id)
    if response:
        return jsonify({"response": response}), 200
    return {"Message": "Business doesn't exist"}


@app.route('/api/v1/businesses/<string:business_id>', methods=['PUT'])
@token_required
def get_update_business(current_user, business_id):
    """
    User must be logged in to update business
    """
    data = request.get_json()
    new_name = data['name']
    new_description = data['description']
    response = business_object.update_business(business_id, new_name, new_description)
    if response:
        return jsonify({"response": response}), 200
    # return jsonify({'Message': 'Business updated'}), 200
    

@app.route('/api/v1/businesses', methods=['GET'])
def get_all_businesses():
    return jsonify({"businesses": business_object.businesses}), 200


# config_name = os.getenv('APP_SETTINGS')
# app = create_app(config_name)
if __name__ == '__main__':
    app.run(debug=True, port=8000)
 