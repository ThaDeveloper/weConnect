from flask import Flask, request, jsonify, make_response,session, Blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
import jwt
import datetime
from functools import wraps
import os
from models import User, Business
from config import app_config

# create a flask app instance

api = Blueprint('app', __name__)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(api)
    return app


# instance of model that will store app data
# application will use data structures to srore data
user_model = User()
business_model = Business()

# def find_user_by_username(username):
#     for user in users:
#         if user['username'] == username:
#             return user

# def find_business_by_id(business_id):
#     for business in businesses:
#         if business['business_id'] == business_id:
#             return business


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'Message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, os.getenv("SECRET_KEY")
            # current_user = find_user_by_username(data['username'])
            if data['username'] in user_model.user_token
                current_user = user_model.users[data['username']]
            return jsonify({"Message": "Token expired"})
        except:
            return jsonify({'Message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@api.route('/api/v1/auth/register',  methods=['POST'])
def create_user():
     """receive user input as json object"""
    data = request.get_json()
    password_hash = sha256_crypt.encrypt(str(data['password']))
    
    if data['username'] in user_model.users:
        return jsonify({'Message': "User already exists"}), 400
    if data['username'] == "" or data['password'] == "":
            return jsonify({'Message': 
                "Username and Password is required"}),400

    data = user_model.create_user(data['username']), password_hash)
    return jsonify({"Message": "User registered successfully"}), 201

  
@app.route('/api/auth/login', methods = ['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"Message": "Auth missing"}), 401
    
    for user in users:
        if auth.username == user['username'] and auth.password == user['password'] :
            token = jwt.encode({'username': auth.username,  'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20)}, app.config['SECRET_KEY'])
        
            return jsonify({"token": token.decode("UTF-8")}), 200# for python3 have to decode to reg string since it's generated in bytes

    return jsonify({"Message": "Invalid login" }),401


@app.route('/api/auth/logout', methods = ['DELETE'])
@token_required
def logout(current_user):
    session.clear()
    return jsonify({"Message": "Logged out"}), 202


@app.route('/api/auth/reset-password', methods=['PUT'])
@token_required
def reset_password(current_user):
    """
    User must be logged in to update password
    """
    data = request.get_json()
    response = find_user_by_username(current_user['username'])
    if data['password']:
        response['password'] = sha256_crypt.encrypt(str(data['password']))
        return jsonify({'Message': 'password updated'}), 200
    return jsonify({'Message': 'password cannot be empty'}), 403


@app.route('/api/auth/users', methods=['GET'])
def get_all_users():
    return jsonify({"users": users}), 200


@app.route('/api/businesses', methods=['POST'])
@token_required
def create_business(current_user):
    new_business = {'business_id': str(uuid.uuid4()), 'user_id': find_user_by_username(current_user['username'])['id'], 'name':  request.json['name'],
                'description': request.json['name'], 'location': request.json['location'], 
                'category': request.json['category']}
            
    for business in businesses:
        if new_business['name'] == business['name']:
            return jsonify({'Message': "Business name already exists"}), 400
        if request.json['name'] == "":
            return jsonify({'Message': 
                "Business name is required"}),400

    businesses.append(new_business)
    return jsonify({"Message": "Business registered successfully"}), 201


@app.route('/api/businesses/<string:business_id>', methods=['GET'])
def get_one_business(business_id):
    """
    User must be logged in to update business
    """
    # data = request.get_json()
    response = find_business_by_id(business_id)
    if response:
        return jsonify({"response": response}), 200
    return {"Message": "no data"}


@app.route('/api/businesses/<string:business_id>', methods=['PUT'])
@token_required
def get_update_business(business_id):
    """
    User must be logged in to update business
    """
    data = request.get_json()
    response = find_business_by_id(business_id)
    if response:
        if data['name']:
            response['name'] = data['name']
            response['description'] = data['description']
            return jsonify({'Message': 'Business updated'}), 200
        return jsonify({'Message': 'Business name cannot be empty'}), 403
    

@app.route('/api/businesses', methods=['GET'])
def get_all_businesses():
    return jsonify({"businesses": businesses}), 200

if __name__ == '__main__':
    app.run(debug=True)
 