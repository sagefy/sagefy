from app import app
from flask import jsonify, abort
from models.user import User
from flask import request


@app.route('/api/users/login/', methods=['POST'])
def login():
    """
    Login user.
    """
    return jsonify(**{})


@app.route('/api/users/logout/', methods=['POST'])
def logout():
    """
    Logout user.
    """
    return jsonify(**{})


@app.route('/api/users/current/', methods=['GET'])
def get_current_user():
    """
    Get current user's information.
    """
    return jsonify(**{})


@app.route('/api/users/<user_id>/', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get user by ID.
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return abort(404)
    return jsonify(user=user.to_dict())


@app.route('/api/users/', methods=['POST'])
def create_user():
    """
    Create user.
    """
    try:
        user = User(request.form)
    except AssertionError as error:
        return jsonify(error=str(error))
    return jsonify(user=user.to_dict())


@app.route('/api/users/<user_id>/', methods=['PUT'])
def update_user(user_id):
    """
    Update user.
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return abort(404)

    return jsonify(**{})


@app.route('/api/users/create_password/', methods=['POST'])
def create_password():
    """
    Create password.
    """
    return jsonify(**{})
