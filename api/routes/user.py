from models.user import User
from flask import Blueprint, jsonify, request, make_response, abort
from flask.ext.login import login_user, current_user, logout_user
from modules.content import get as c


user = Blueprint('user', __name__, url_prefix='/api/users')


def _login(user):
    """
    Login a given user, and return an appropriate response.
    Used by signup, login, and reset password.
    """
    login_user(user, remember=True)
    resp = make_response(jsonify(user=user.deliver(access='private')))
    resp.set_cookie('logged_in', '1')
    return resp


@user.route('/<user_id>/', methods=['GET'])
def get_user(user_id):
    """Get the user by their ID."""
    user = User.get(id=user_id)
    if user:
        return jsonify(
            user=user.deliver(
                access='private' if user.is_current_user() else None
            )
        )
    return abort(404)


@user.route('/current/', methods=['GET'])
def get_current_user():
    """Get current user's information."""
    if current_user.is_authenticated():
        return jsonify(user=current_user.deliver(access='private'))
    return abort(401)


@user.route('/', methods=['POST'])
def create_user():
    """Create user."""
    user, errors = User.insert(request.json)
    if len(errors):
        return jsonify(errors=errors), 400
    return _login(user)


@user.route('/login/', methods=['POST'])
def login():
    """Login user."""
    user = User.get(name=request.json.get('name'))
    if not user:
        return jsonify(errors=[{
            'name': 'name',
            'message': c('user', 'no_user'),
        }]), 404
    if not user.is_password_valid(request.json.get('password')):
        return jsonify(errors=[{
            'name': 'password',
            'message': c('user', 'no_match'),
        }]), 400
    return _login(user)


@user.route('/logout/', methods=['POST'])
def logout():
    """Logout user."""
    logout_user()
    resp = make_response('')
    resp.set_cookie('logged_in', '0')
    return resp, 204


@user.route('/<user_id>/', methods=['PUT'])
def update_user(user_id):
    """Update the user. Must be the current user."""
    user = User.get(id=user_id)
    if not user:
        return abort(404)
    if not user.is_current_user():
        return abort(401)
    user, errors = user.update(request.json)
    if len(errors):
        return jsonify(errors=errors), 400
    return jsonify(user=user.deliver(access='private'))


@user.route('/token/', methods=['POST'])
def create_token():
    """Create an email token for the user."""
    user = User.get(email=request.json.get('email'))
    if not user:
        return abort(404)
    user.get_email_token()
    return '', 204


@user.route('/password/', methods=['POST'])
def create_password():
    """Update a user's password if the token is valid."""
    user = User.get(id=request.json.get('id'))
    if not user:
        return abort(404)
    valid = user.is_valid_token(request.json.get('token'))
    if not valid:
        return abort(403)
    user.update_password(request.json.get('password'))
    return _login(user)


@user.route('/<user_id>/menu/', methods=['GET'])
def get_menu(user_id):
    """TODO
    Get the list of menu items given the user's context.
    """
    pass


@user.route('/<user_id>/sets/', methods=['GET'])
def get_user_sets(user_id):
    """TODO
    Get the list of sets the user has added.
    """
    pass


@user.route('/<user_id>/sets/', methods=['POST'])
def add_set(user_id):
    """TODO
    Add a set to the learner's list of sets.
    """
    pass


@user.route('/<user_id>/sets/<set_id>/', methods=['DELETE'])
def remove_set(user_id, set_id):
    """TODO
    Remove a set from the learner's list of sets.
    """
    pass
