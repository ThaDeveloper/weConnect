from flask import Flask, request, jsonify
import uuid
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY']= 'doordonotthereisnotry'

users = [
]
@app.route('/api/auth/register', methods=['POST'])
def create_user():
    user = {'username' : request.json['username'],'password' : request.json['password'], 'id':len(users)+1}
    for u in users:
        if request.json['username'] in u.values():
            return jsonify({'Message': "User alread exists"}),400
    users.append(user)
    return jsonify({'Message':'User registered successfully'}),201


if __name__=='__main__':
    app.run(debug=True)

