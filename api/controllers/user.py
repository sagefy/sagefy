from app import app
from flask import jsonify


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
    return jsonify(**{})


@app.route('/api/users/', methods=['POST'])
def create_user(user_id):
    """
    Create user.
    """
    return jsonify(**{})


@app.route('/api/users/<user_id>/', methods=['PUT'])
def update_user(user_id):
    """
    Update user.
    """
    return jsonify(**{})


@app.route('/api/users/create_password/', methods=['POST'])
def create_password():
    """
    Create password.
    """
    return jsonify(**{})
