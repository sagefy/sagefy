from models.user import User
from models.user_sets import UserSets
from models.follow import Follow
from modules.content import get as c
from modules.discuss import get_posts_facade

from framework.routes import get, post, put, delete, abort
from framework.session import get_current_user, log_in_user, log_out_user


def _log_in(user):
    """
    Log in a given user, and return an appropriate response.
    Used by sign up, log in, and reset password.
    """

    session_id = log_in_user(user)
    if session_id:
        return 200, {
            'user': user.deliver(access='private'),
            'cookies': {
                'session_id': session_id
            },
        }
    return abort(401)


@get('/s/users/current')
def get_current_user_route(request):
    """
    Get current user's information.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    return 200, {'user': current_user.deliver(access='private')}


@get('/s/users/{user_id}')
def get_user_route(request, user_id):
    """
    Get the user by their ID.
    """

    db_conn = request['db_conn']
    user = User.get(db_conn, id=user_id)
    current_user = get_current_user(request)
    # Posts if in request params
    # Sets if in request params and allowed
    # Follows if in request params and allowed
    if not user:
        return abort(404)

    data = {}
    data['user'] = user.deliver(access='private'
                                if current_user
                                and user['id'] == current_user['id']
                                else None)

    # TODO-2 SPLITUP create new endpoints for these instead
    if 'posts' in request['params']:
        data['posts'] = [post.deliver() for post in
                         get_posts_facade(db_conn, user_id=user['id'])]
    if ('sets' in request['params']
            and user['settings']['view_sets'] == 'public'):
        u_sets = UserSets.get(db_conn, user_id=user['id'])
        data['sets'] = [set_.deliver() for set_ in u_sets.list_sets(db_conn)]
    if ('follows' in request['params']
            and user['settings']['view_follows'] == 'public'):
        data['follows'] = [follow.deliver() for follow in
                           Follow.list(db_conn, user_id=user['id'])]
    if 'avatar' in request['params']:
        size = int(request['params']['avatar'])
        data['avatar'] = user.get_avatar(size if size else None)

    return 200, data


@post('/s/users')
def create_user_route(request):
    """
    Create user.
    """

    db_conn = request['db_conn']
    user, errors = User.insert(db_conn, request['params'])
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'YEcBnqf4vyA2pckIy70R789B',
        }
    return _log_in(user)


@post('/s/sessions')
def log_in_route(request):
    """
    Log in user.
    """

    db_conn = request['db_conn']
    name = request['params'].get('name') or ''
    name = name.lower().strip()

    user = User.get(db_conn, name=name)
    if not user:
        user = User.get(db_conn, email=request['params'].get('name'))
    if not user:
        return 404, {
            'errors': [{
                'name': 'name',
                'message': c('no_user'),
            }],
            'ref': 'FYIPOI8g2nzrIEcJYSDAfmti'
        }
    if not user.is_password_valid(request['params'].get('password')):
        return 400, {
            'errors': [{
                'name': 'password',
                'message': c('no_match'),
            }],
            'ref': 'UwCRydZ7Agi7LYKv9c1y07ft'
        }
    return _log_in(user)


@delete('/s/sessions')
def log_out_route(request):
    """
    Log out user.
    """

    log_out_user(request)
    return 200, {
        'cookies': {
            'session_id': None
        }
    }


@put('/s/users/{user_id}')
def update_user_route(request, user_id):
    """
    Update the user. Must be the current user.
    """

    db_conn = request['db_conn']
    user = User.get(db_conn, id=user_id)
    current_user = get_current_user(request)
    if not user:
        return abort(404)
    if not user['id'] == current_user['id']:
        return abort(401)
    user, errors = user.update(db_conn, request['params'])
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'AS7LCAWiOOyeEbNOrbsegVY9',
        }
    return 200, {'user': user.deliver(access='private')}


@post('/s/password_tokens')
def create_token_route(request):
    """
    Create an email token for the user.
    """

    db_conn = request['db_conn']
    user = User.get(db_conn, email=request['params'].get('email'))
    if not user:
        return abort(404)
    user.get_email_token()
    return 200, {}


@post('/s/users/{user_id}/password')
def create_password_route(request, user_id):
    """
    Update a user's password if the token is valid.
    """

    db_conn = request['db_conn']
    user = User.get(db_conn, id=user_id)
    if not user:
        return abort(404)
    valid = user.is_valid_token(request['params'].get('token'))
    if not valid:
        return abort(403)
    user['password'] = request['params'].get('password')
    user.save(db_conn)
    return _log_in(user)
