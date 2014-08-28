from models.user import User
from flask import Blueprint, jsonify, request, make_response
from flask.ext.login import login_user, current_user, logout_user


user = Blueprint('user', __name__, url_prefix='/api/users')


@user.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get the user by their ID."""
    user = User.get(id=user_id)
    if user:
        return jsonify(user=user.deliver(private=user.is_current_user()))
    return jsonify(errors=[{'message': 'No user found.'}]), 404


@user.route('/current', methods=['GET'])
def get_current_user():
    """Get current user's information."""
    if current_user.is_authenticated():
        return jsonify(user=current_user.deliver(private=True))
    return jsonify(errors=[{'message': 'Not logged in.'}]), 404


@user.route('/', methods=['POST'])
def create_user():
    """Create user."""
    user, errors = User.insert(request.json)
    if len(errors) == 0:
        login_user(user, remember=True)
        resp = make_response(jsonify(user=user.deliver(private=True)))
        resp.set_cookie('logged_in', '1')
        return resp
    else:
        return jsonify(errors=errors), 401


@user.route('/login', methods=['POST'])
def login():
    """Login user."""
    user = User.get(name=request.json.get('name'))
    if not user:
        return jsonify(errors=[{
            'name': 'name',
            'message': 'No user by that name.',
        }]), 404
    if user.is_password_valid(request.json.get('password')):
        login_user(user, remember=True)
        resp = make_response(jsonify(user=user.deliver(private=True)))
        resp.set_cookie('logged_in', '1')
        return resp
    return jsonify(errors=[{
        'name': 'password',
        'message': 'Name and password do not match.',
    }]), 404


@user.route('/logout', methods=['POST'])
def logout():
    """Logout user."""
    logout_user()
    resp = make_response('')
    resp.set_cookie('logged_in', '0')
    return resp, 204


@user.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update the user. Must be the current user."""
    user = User.get(id=user_id)

    if not user:
        return jsonify(errors=[{
            "message": "User not found."
        }]), 404

    if not user.is_current_user():
        return jsonify(errors=[{
            "message": "Not authorized."
        }]), 401

    user, errors = user.update(request.json)
    if len(errors) == 0:
        return jsonify(user=user.deliver(private=True))
    else:
        return jsonify(errors=errors), 400


@user.route('/token', methods=['POST'])
def create_token():
    """Create an email token for the user."""
    user = User.get(email=request.json.get('email'))
    if not user:
        return jsonify(errors=[{"message": "User not found."}]), 404
    user.get_email_token()
    return '', 204


@user.route('/password', methods=['POST'])
def create_password():
    """Update a user's password if the token is valid."""
    user = User.get(id=request.json.get('id'))
    valid = user.is_valid_token(request.json.get('token'))
    if not valid:
        return jsonify(errors=[{"message": "Token not found."}]), 404
    user.update_password(request.json.get('password'))
    login_user(user, remember=True)
    resp = make_response(jsonify(user=user.deliver(private=True)))
    resp.set_cookie('logged_in', '1')
    return resp
