from models.user import User
from models.user_sets import UserSets
from models.follow import Follow
from flask import Blueprint, jsonify, request, make_response, abort
from flask.ext.login import login_user, current_user, logout_user
from modules.content import get as c
from modules.util import parse_args
from modules.discuss import get_posts_facade


user_routes = Blueprint('user', __name__, url_prefix='/api/users')


def _log_in(user):
    """
    Log in a given user, and return an appropriate response.
    Used by sign up, log in, and reset password.
    """

    login_user(user, remember=True)
    resp = make_response(jsonify(user=user.deliver(access='private')))
    resp.set_cookie('logged_in', '1')
    return resp


@user_routes.route('/<user_id>/', methods=['GET'])
def get_user(user_id):
    """
    Get the user by their ID.
    """

    user = User.get(id=user_id)
    # Posts if in request params
    # Sets if in request params and allowed
    # Follows if in request params and allowed
    if not user:
        return abort(404)

    args = parse_args(request.args)

    data = {}
    data['user'] = user.deliver(access='private'
                                if user.is_current_user()
                                else None)
    if 'posts' in args:
        data['posts'] = [post.deliver() for post in
                         get_posts_facade(user_id=user['id'])]
    if 'sets' in args and user['settings']['view_sets'] == 'public':
        u_sets = UserSets.get(user_id=user['id'])
        data['sets'] = [set_.deliver() for set_ in u_sets.list_sets()]
    if 'follows' in args and user['settings']['view_follows'] == 'public':
        data['follows'] = [follow.deliver() for follow in
                           Follow.list(user_id=user['id'])]
    return jsonify(**data)


@user_routes.route('/current/', methods=['GET'])
def get_current_user():
    """
    Get current user's information.
    """

    if not current_user.is_authenticated():
        return abort(401)
    return jsonify(user=current_user.deliver(access='private'))


@user_routes.route('/', methods=['POST'])
def create_user():
    """
    Create user.
    """

    user, errors = User.insert(request.json)
    if len(errors):
        return jsonify(errors=errors), 400
    return _log_in(user)


@user_routes.route('/log_in/', methods=['POST'])
def log_in():
    """
    Log in user.
    """

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
    return _log_in(user)


@user_routes.route('/log_out/', methods=['POST'])
def log_out():
    """
    Log out user.
    """

    logout_user()
    resp = make_response('')
    resp.set_cookie('logged_in', '0')
    return resp, 204


@user_routes.route('/<user_id>/', methods=['PUT'])
def update_user(user_id):
    """
    Update the user. Must be the current user.
    """

    user = User.get(id=user_id)
    if not user:
        return abort(404)
    if not user.is_current_user():
        return abort(401)
    user, errors = user.update(request.json)
    if len(errors):
        return jsonify(errors=errors), 400
    return jsonify(user=user.deliver(access='private'))


@user_routes.route('/token/', methods=['POST'])
def create_token():
    """
    Create an email token for the user.
    """

    user = User.get(email=request.json.get('email'))
    if not user:
        return abort(404)
    user.get_email_token()
    return '', 204


@user_routes.route('/password/', methods=['POST'])
def create_password():
    """
    Update a user's password if the token is valid.
    """

    user = User.get(id=request.json.get('id'))
    if not user:
        return abort(404)
    valid = user.is_valid_token(request.json.get('token'))
    if not valid:
        return abort(403)
    user.update_password(request.json.get('password'))
    return _log_in(user)
