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
from src.models import Business, Review, ValidationError
from src.utils import validate_user
from src.auth import token_required

biz = Blueprint('business', __name__)


@biz.route('/businesses', methods=['POST'])
@token_required
def create_business(current_user):
    """Logged in users to create business"""
    data = request.get_json()
    try:
        # validates user key/value inputs using a try-catch block
        business = Business()
        sanitized = business.import_data(data)
        if sanitized == "Invalid":
            return jsonify({"Message": "A business must have a name"}), 400
    except ValidationError as e:
        return jsonify({"Message": str(e)}), 400

    duplicate = Business.query.filter_by(name=data['name']).first()
    if not duplicate:
        business.user_id = current_user.id
        business.add()
        return jsonify({"Message": "Business registered successfully"}), 201
    return jsonify({"Message": "Business already exist"}), 400


@biz.route('/businesses/<int:id>', methods=['GET'])
def get_one_business(id):
    """Return a single business"""
    business = Business.query.filter_by(id=id).first()
    if not business:
        return jsonify({'Message': 'Business not found'}), 404
    biz_data = {}
    biz_data['id'] = business.id
    biz_data['name'] = business.name
    biz_data['description'] = business.description
    biz_data['location'] = business.location
    biz_data['category'] = business.category
    biz_data['user_id'] = business.user_id
    biz_data['created_at'] = business.created_at
    biz_data['updated_at'] = business.updated_at
    return jsonify({"business": biz_data}), 200


@biz.route('/businesses', methods=['GET'])
def get_all_businesses():
    businesses = Business.query.all()
    output = []
    for business in businesses:
        biz_data = {}
        biz_data['id'] = business.id
        biz_data['name'] = business.name
        biz_data['description'] = business.description
        biz_data['location'] = business.location
        biz_data['category'] = business.category
        biz_data['user_id'] = business.user_id
        biz_data['created_at'] = business.created_at
        biz_data['updated_at'] = business.updated_at
        output.append(biz_data)
    return jsonify({"businesses": output}), 200


@biz.route('/businesses/<int:business_id>', methods=['PUT'])
@token_required
def get_update_business(current_user, business_id):
    """
    User must be logged in to update business
    """
    data = request.get_json()
    new_name = data['name']
    new_description = data['description']
    business = business_object.find_business_by_id(business_id)
    if business:
        if current_user['username'] == business['user_id']:
            response = business_object.update_business(business_id,
                                                       new_name,
                                                       new_description)
            if response:
                if new_name not in business_object.businesses:
                    return jsonify({'Message': 'Business updated'}), 200
                return jsonify({'Message':
                                'Business name already exists'}), 400
        return jsonify({"Message":
                        "Unauthorized:You can only update your own" +
                        "business!!"}), 401
    return jsonify({'Message': 'Business not found'}), 404


@biz.route('/businesses/<int:business_id>', methods=['DELETE'])
@token_required
def remove_business(current_user, business_id):
    """Remove business by id"""
    business = business_object.find_business_by_id(business_id)
    if business:
        if current_user['username'] == business['user_id']:
            del business_object.businesses[business['name']]
            return jsonify({"Message": "Business deleted successfully"}), 200
        return jsonify({"Message":
                        "Unauthorized:You can only delete" +
                        "your own business!!"}), 401
    return jsonify({"Message": "Business not found"}), 404


@biz.route('/businesses/<int:business_id>/reviews', methods=['POST'])
@token_required
def create_review(current_user, business_id):
    """ User can only review a business if logged in"""
    data = request.get_json()
    if not data or not data['title']:
        return jsonify({"Message": "Review title is required"}), 400

    business = business_object.find_business_by_id(business_id)
    if business:
        user_id = current_user['username']
        review_object.add_review(data['title'],
                                 data['message'],
                                 user_id,
                                 business_id)
        return jsonify({"Message": "Your review has been recorded"}), 201

    return jsonify({"Message": "Business not found"}), 401


@biz.route('/businesses/<int:business_id>/reviews', methods=['GET'])
@token_required
def get_business_reviews(current_user, business_id):
    """List all business' reviews"""
    business = business_object.find_business_by_id(business_id)
    if business:
        reviews = review_object.get_reviews(business_id)
        return jsonify({"Reviews": reviews}), 200
    return jsonify({"Message": "Business not found"}), 401
