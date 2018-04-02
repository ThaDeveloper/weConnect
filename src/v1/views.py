import os
import sys
import inspect
from flask import request, jsonify, Blueprint
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from src.v1.models import Business, Reviews
from src.v1.auth import token_required

business_object = Business()
review_object = Reviews()
biz = Blueprint('v1_business', __name__)


@biz.route('/businesses', methods=['POST'])
@token_required
def create_business(current_user):
    """Logged in users to create business"""
    data = request.get_json()
    if not data or not data['name']:
        return jsonify({"Message": "Name is required!"}), 400

    if data['name'] in business_object.businesses:
        return jsonify({"Message": "Name already exists!"}), 400
    user_id = current_user['username']
    business_object.register_business(data['name'],
                                      data['description'], data['location'],
                                      data['category'], user_id)
    return jsonify({"Message": "Business registered successfully"}), 201


@biz.route('/businesses/<int:business_id>', methods=['GET'])
def get_one_business(business_id):
    """Return a single business"""
    response = business_object.find_business_by_id(business_id)
    if response:
        return jsonify({"Business Profile": response}), 200
    return jsonify({"Message": "Business not found"}), 404


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


@biz.route('/businesses', methods=['GET'])
def get_all_businesses():
    return jsonify({"businesses": business_object.businesses}), 200


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
