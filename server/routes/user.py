from modules.content import get as c
from framework.routes import get, post, put, delete, abort
from framework.session import get_current_user, log_in_user, log_out_user
from database.user import get_user, insert_user, deliver_user, get_avatar, \
    update_user, is_password_valid, get_email_token, is_valid_token, \
    update_user_password, list_users_by_user_ids


def _log_in(user):
    """
    Log in a given user, and return an appropriate response.
    Used by sign up, log in, and reset password.
    """

    session_id = log_in_user(user)
    if session_id:
        return 200, {
            'user': deliver_user(user, access='private'),
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
    return 200, {'user': deliver_user(current_user, access='private')}


@get('/s/users/{user_id}')
def get_user_route(request, user_id):
    """
    Get the user by their ID.
    """

    db_conn = request['db_conn']
    user = get_user({'id': user_id}, db_conn)
    if not user:
        return abort(404)
    current_user = get_current_user(request)
    access = 'private' if (current_user and
                           user['id'] == current_user['id']) else None
    data = {'user': deliver_user(user, access)}
    if 'avatar' in request['params']:
        size = int(request['params']['avatar']) or None
        data['avatar'] = get_avatar(user['email'], size)
    return 200, data


@get('/s/users')
def list_users_route(request):
    """
    List users by user id. Public facing route.
    """

    db_conn = request['db_conn']
    user_ids = request['params'].get('user_ids')
    if not user_ids:
        return abort(404)
    user_ids = user_ids.split(',')
    users = list_users_by_user_ids(user_ids, db_conn)
    if not users:
        return abort(404)
    size = int(request['params'].get('avatar') or 0) or None
    avatars = {
        user['id']: get_avatar(user['email'], size)
        for user in users
    }
    return 200, {
        'users': [deliver_user(user, None) for user in users],
        'avatars': avatars,
    }


@post('/s/users')
def create_user_route(request):
    """
    Create user.
    """

    db_conn = request['db_conn']
    user, errors = insert_user(request['params'], db_conn)
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
    user = get_user({'name': name}, db_conn)
    if not user:
        user = get_user({'email': name}, db_conn)
    if not user:
        return 404, {
            'errors': [{
                'name': 'name',
                'message': c('no_user'),
            }],
            'ref': 'FYIPOI8g2nzrIEcJYSDAfmti'
        }
    real_encrypted_password = user['password']
    given_password = request['params'].get('password')
    if not is_password_valid(real_encrypted_password, given_password):
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
    user = get_user({'id': user_id}, db_conn)
    current_user = get_current_user(request)
    if not user:
        return abort(404)
    if not user['id'] == current_user['id']:
        return abort(401)
    user, errors = update_user(user, request['params'], db_conn)
    if len(errors):
        return 400, {
            'errors': errors,
            'ref': 'AS7LCAWiOOyeEbNOrbsegVY9',
        }
    return 200, {'user': deliver_user(user, access='private')}


@post('/s/password_tokens')
def create_token_route(request):
    """
    Create an email token for the user.
    """

    db_conn = request['db_conn']
    user = get_user({'email': request['params'].get('email')}, db_conn)
    if not user:
        return abort(404)
    get_email_token(user)
    return 200, {}


@post('/s/users/{user_id}/password')
def create_password_route(request, user_id):
    """
    Update a user's password if the token is valid.
    """

    db_conn = request['db_conn']
    user = get_user({'id': user_id}, db_conn)
    if not user:
        return abort(404)
    token = request['params'].get('token')
    valid = is_valid_token(user, token)
    if not valid:
        return abort(403)
    given_password = request['params'].get('password')
    update_user_password(user, {'password': given_password}, db_conn)
    return _log_in(user)
