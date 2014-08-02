from app import app
from models.user import User
from flask import jsonify
from flask import request
from flask import make_response
from flask.ext.login import login_user, current_user, logout_user


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get the user by their ID.
    """
    user = User.get(id=user_id)
    if user:
        return jsonify(user=user.get_fields())
    return jsonify(errors=[{'message': 'No user found.'}]), 404


@app.route('/api/users/current', methods=['GET'])
def get_current_user():
    """
    Get current user's information.
    """

    if current_user.is_authenticated():
        return jsonify(user=current_user.get_fields())
    return jsonify(errors=[{'message': 'Not logged in.'}]), 404


@app.route('/api/users/', methods=['POST'])
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


@app.route('/api/users/login', methods=['POST'])
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


@app.route('/api/users/logout', methods=['POST'])
def logout():
    """
    Logout user.
    """

    logout_user()
    resp = make_response('')
    resp.set_cookie('logged_in', '0')
    return resp, 204

# @app.route('/api/users/<user_id>', methods=['PUT'])
# def update_user(user_id):
#     """
#     Update user.
#     Create a new password after the token has been created.
#     """

#     # TODO: test route

#     user = User.get_by_id(user_id)

#     # TODO: should this be two routes?

#     if 'password' in request.form:
#         user = User.get_by_token(request.form.get('token'))

#         if user:
#             user.password = request.form.get('password')
#             return jsonify(message='Password updated.'), 204

#         return jsonify(message='User not found.'), 404

#     if user.id == current_user.id:
#         try:
#             user.update(request.form)
#             return jsonify(user=user)
#         except AssertionError as error:
#             return jsonify(errors=list(error)), 401

#     return jsonify(message='Not authorized to update user.'), 401


# @app.route('/api/users/request_password_token', methods=['GET', 'POST'])
# def request_password_token():
#     """
#     Request a token to update the password.
#     """

#     # TODO: test route

#     if current_user.is_authenticated():
#         user = current_user
#     else:
#         user = User.get_by_email(request.form.get('email'))

#     user.send_password_token()
#     return jsonify(message='Password token sent via email.'), 201
