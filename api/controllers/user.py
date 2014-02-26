from app import app
from flask import jsonify
from models.user import User
from flask import request
from flask.ext.login import login_user, logout_user, current_user


@app.route('/api/users/', methods=['POST'])
def create_user():
    """
    Create user.
    """

    # TODO: test route

    try:
        user = User(request.form)
    except AssertionError as error:
        return jsonify(error=str(error))
    return jsonify(user=user.to_dict())


@app.route('/api/users/<user_id>/', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get user by ID.
    """

    # TODO: test route

    user = User.get_by_id(user_id)

    if user and user.id == current_user.id:
        return jsonify(user=user.to_dict_secure())
    if user:
        return jsonify(user=user.to_dict())
    return jsonify(message='No user found.'), 404


@app.route('/api/users/current/', methods=['GET'])
def get_current_user():
    """
    Get current user's information.
    """

    # TODO: test route

    if current_user.is_authenticated():
        return jsonify(user=current_user.to_dict_secure())
    return jsonify(message='Not logged in.'), 404


@app.route('/api/users/<user_id>/', methods=['PUT'])
def update_user(user_id):
    """
    Update user.
    Create a new password after the token has been created.
    """

    # TODO: test route

    user = User.get_by_id(user_id)

    # TODO: should this be two routes?

    if 'password' in request.form:
        user = User.get_by_token(request.form.get('token'))

        if user:
            user.password = request.form.get('password')
            login_user(user)
            return jsonify(message='Password updated.'), 204

        return jsonify(message='User not found.'), 404

    if user.id == current_user.id:
        try:
            user.update(request.form)
            return jsonify(user=user)
        except AssertionError as error:
            return jsonify(error=str(error))

    return jsonify(message='Not authorized to update user.'), 401


@app.route('/api/users/login/', methods=['POST'])
def login():
    """
    Login user.
    """

    # TODO: test route

    user = User.get_by_email(request.form.get('email'))

    if user and user.is_password_valid(request.form.get('password')):
        login_user(user)
        return jsonify(user=user)

    return jsonify(message='Email and password do not match.'), 404


@app.route('/api/users/logout/', methods=['POST'])
def logout():
    """
    Logout user.
    """

    # TODO: test route

    logout_user()
    return jsonify(message='Successfully logged out.'), 204

    # TODO: message different if not currently logged in


@app.route('/api/users/request_password_token/', methods=['GET', 'POST'])
def request_password_token():
    """
    Request a token to update the password.
    """

    # TODO: test route

    if current_user.is_authenticated():
        user = current_user
    else:
        user = User.get_by_email(request.form.get('email'))

    user.send_password_token()
    return jsonify(message='Password token sent via email.'), 201
