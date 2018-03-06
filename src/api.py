from flask import Flask, request, jsonify, make_response,session
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
import jwt
import datetime
from functools import wraps
# from models import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'doordonotthereisnotry'


users = [
]

businesses = [

]
def find_user_by_username(username):
    for user in users:
        if user['username'] == username:
            return user

def find_business_by_id(business_id):
    for business in businesses:
        if business['business_id'] == business_id:
            return business


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
            current_user = find_user_by_username(data['username'])
        except:
            return jsonify({'Message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app .route('/api/auth/register',  methods=['POST'])
def create_user():
    new_user = {'id': str(uuid.uuid4()), 'username':  request.json['username'],
                'password': sha256_crypt.encrypt(str(request.json['password'])), "admin": False}
    for user in users:
        if new_user['username'] == user['username']:
            return jsonify({'Message': "User already exists"}), 400
        if request.json['username'] == "" or request.json['password'] == "":
            return jsonify({'Message': 
                "Username and Password is required"}),400

    users.append(new_user)
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

    

@app.route('/api/businesses', methods=['GET'])
def get_all_businesses():
    return jsonify({"businesses": businesses}), 200

if __name__ == '__main__':
    app.run(debug=True)
 