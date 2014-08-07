from models.user import User
from flask import Blueprint, jsonify, request, make_response
from flask.ext.login import login_user, current_user, logout_user


user = Blueprint('user', __name__, url_prefix='/api/users')


@user.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get the user by their ID.
    """
    user = User.get(id=user_id)
    if user:
        return jsonify(user=user.get_fields())
    return jsonify(errors=[{'message': 'No user found.'}]), 404


@user.route('/current', methods=['GET'])
def get_current_user():
    """
    Get current user's information.
    """
    if current_user.is_authenticated():
        return jsonify(user=current_user.get_fields())
    return jsonify(errors=[{'message': 'Not logged in.'}]), 404


@user.route('/', methods=['POST'])
def create_user():
    """
    Create user.
    """
    user = User(request.json)
    valid, errors = user.insert()
    if valid:
        login_user(user, remember=True)
        resp = make_response(jsonify(user=user.get_fields()))
        resp.set_cookie('logged_in', '1')
        return resp
    else:
        return jsonify(errors=errors), 401


@user.route('/login', methods=['POST'])
def login():
    """
    Login user.
    """
    user = User.get(name=request.json.get('name'))
    if not user:
        return jsonify(errors=[{
            'name': 'name',
            'message': 'No user by that name.',
        }]), 404
    if user.is_password_valid(request.json.get('password')):
        login_user(user, remember=True)
        resp = make_response(jsonify(user=user.get_fields()))
        resp.set_cookie('logged_in', '1')
        return resp
    return jsonify(errors=[{
        'name': 'password',
        'message': 'Name and password do not match.',
    }]), 404


@user.route('/logout', methods=['POST'])
def logout():
    """
    Logout user.
    """
    logout_user()
    resp = make_response('')
    resp.set_cookie('logged_in', '0')
    return resp, 204


@user.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """

    """
    user = User.get(id=user_id)

    if not user:
        return jsonify(errors=[{
            "message": "User not found."
        }]), 404

    if not user.is_current_user():
        return jsonify(errors=[{
            "message": "Not authorized."
        }]), 401

    valid, errors = user.update(request.json)
    if valid:
        return jsonify(user=user.get_fields())
    else:
        return jsonify(errors=errors), 400
