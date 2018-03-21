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
from src.v2.models import Business, Review, ValidationError
from src.utils import validate_user
from src.v2.auth import token_required

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


@biz.route('/businesses/<int:id>', methods=['PUT'])
@token_required
def get_update_business(current_user, id):
    """
    User must be logged in to update business
    """
    data = request.get_json()
    business = Business.query.filter_by(id=id).first()
    if business:
        if current_user.id == business.user_id:
            # to get specific messages we only filter by name not name and
            # owner
            duplicate = Business.query.filter_by(name=data['name']).first()
            if not duplicate or business.name == data['name']:
                business.name = data['name']
                business.description = data['description']
                business.location = data['location']
                business.category = data['category']
                business.add()
                return jsonify({'Message': 'Business updated'}), 200
            return jsonify({'Message':
                            'Business name already exists'}), 400
        return jsonify({"Message":
                        "Unauthorized:You can only update your own" +
                        " business!!"}), 401
    return jsonify({'Message': 'Business not found'}), 404


@biz.route('/businesses/<int:id>', methods=['DELETE'])
@token_required
def remove_business(current_user, id):
    """Remove business by id"""
    business = Business.query.filter_by(id=id).first()
    if not business:
        return jsonify({'Message': 'Business not found'}), 404
    if current_user.id == business.user_id:
        business.delete()
        return jsonify({"Message": "Business deleted successfully"}), 200
    return jsonify({"Message":
                    "Unauthorized:You can only delete" +
                    "your own business!!"}), 401


@biz.route('/businesses/<int:id>/reviews', methods=['POST'])
@token_required
def create_review(current_user, id):
    """ User can only review a business if logged in"""
    business = Business.query.filter_by(id=id).first()
    if not business:
        return jsonify({'Message': 'Business not found'}), 404
    else:
        try:
            review = Review()
            sanitized = review.import_data(request.json)
            if sanitized == "Invalid":
                return jsonify(
                    {"Message": "The review must have a title"}), 400
        except ValidationError as e:
            return jsonify({"Message": str(e)}), 400

        review.user_id = current_user.id
        review.business_id = business.id
        review.add()
        return jsonify({"Message": "Your review has been recorded"}), 201


@biz.route('/businesses/<int:id>/reviews', methods=['GET'])
@token_required
def get_business_reviews(current_user, id):
    """List all business' reviews"""
    business = Business.query.filter_by(id=id).first()
    if not business:
        return jsonify({'Message': 'Business not found'}), 404
    reviews = Review.query.filter_by(business_id=id)
    output = []
    for review in reviews:
        review_data = {}
        review_data['id'] = review.id
        review_data['title'] = review.title
        review_data['message'] = review.message
        review_data['user_id'] = review.user_id
        review_data['created_at'] = review.created_at
        output.append(review_data)
    return jsonify({"Reviews": output}), 200
