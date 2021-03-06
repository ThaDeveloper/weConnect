import os
import sys
import inspect
from flask import request, jsonify, Blueprint
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from src.v2.models import Business, Review, ValidationError
from src.v2.auth import token_required

biz = Blueprint('v2_business', __name__)


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
            return jsonify({"Message": "A business name is required"}), 400
    except ValidationError as e:
        return jsonify({"Message": str(e)}), 400

    duplicate = Business.query.filter_by(name=data['name']).first()
    if not duplicate:
        business.user_id = current_user.id
        business.add()
        return jsonify({"Message": "Business registered successfully"}), 201
    return jsonify({"Message": "Business already exists"}), 400


@biz.route('/businesses/<int:id>', methods=['GET'])
def get_one_business(id):
    """Return a single business"""
    business = Business.query.filter_by(id=id).first()
    if not business:
        return jsonify({'Message': 'Business not found'}), 400
    return jsonify({
        'businesses': [
            {
                'id': business.id,
                'name': business.name,
                'description': business.description,
                'location': business.location,
                'category': business.category,
                'owner': business.owner.first_name + ' ' + business.owner.last_name,
                'created_at': business.created_at,
                'updated_at': business.updated_at
            }
        ]
    }), 200


@biz.route('/businesses/', methods=['GET'])
def get_all_businesses():

    params = {
        'page': request.args.get('page', default=1, type=int),
        'limit': request.args.get('limit', default=5, type=int),
        'location': request.args.get('location', default=None, type=str),
        'category': request.args.get('category', default=None, type=str),
        'query': request.args.get('q', default=None, type=str)
    }
    businesses = Business().search(params)
    if businesses:
        return jsonify({
            'businesses': [
                {
                    'id': business.id,
                    'name': business.name,
                    'description': business.description,
                    'location': business.location,
                    'category': business.category,
                    'owner': business.owner.first_name + ' ' + business.owner.last_name,
                    'created_at': business.created_at,
                    'updated_at': business.updated_at
                } for business in businesses
            ]
        }), 200
    return jsonify({"Message": "No available business"}), 400


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
        return jsonify({'Message': 'Business not found'}), 400
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
def get_business_reviews(id):
    """List all business' reviews"""
    business = Business.query.filter_by(id=id).first()
    if not business:
        return jsonify({'Message': 'Business not found'}), 400
    reviews = Review.query.filter_by(business_id=id)
    if reviews:
        return jsonify({
            'Reviews': [
                {
                    'id': review.id,
                    'title': review.title,
                    'message': review.message,
                    'reviewer': review.reviewer.username,
                    'create_at': review.created_at
                } for review in reviews
            ]
        }), 200
    return jsonify({"Message": "No reviews for this business"})
