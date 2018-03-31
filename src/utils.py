from flask import jsonify


class ValidationError(ValueError):
    pass


def validate_user(data):
    if not isinstance(data['username'], str):
        return jsonify({"Message":
                        "Wrong username format: Can only be a string"}), 400
    if len(
            data['username'].strip()) == 0 or len(
            data["password"].strip()) == 0:
        return jsonify({'Message':
                        "Username and Password is required"}), 400
    for x in data['username']:
        if x.isspace():
            return jsonify({"Message":
                            "Username can't contain spaces"}), 400
    if len(data['username'].strip()) < 3:
        return jsonify({"Message":
                        "Username must be 3 characters and above"}), 400
    if len(
            data['first_name'].strip()) == 0 or len(
            data["last_name"].strip()) == 0:
        return jsonify({'Message':
                        "First Name and Last Name is required"}), 400
