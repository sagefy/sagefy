from modules.content import get as c
from framework.routes import get, post, put, delete, abort
from framework.session import get_current_user, log_in_user, log_out_user
from database.user import get_user, insert_user, deliver_user, get_avatar, \
    update_user, is_password_valid, get_email_token, is_valid_token, \
    update_user_password
from database.follow import list_follows, deliver_follow
from database.user_subjects import list_user_subjects_entity
from database.post import list_posts, deliver_post


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
    current_user = get_current_user(request)
    # Posts if in request params
    # Subjects if in request params and allowed
    # Follows if in request params and allowed
    if not user:
        return abort(404)

    data = {}
    data['user'] = deliver_user(user,
                                access='private'
                                if current_user
                                and user['id'] == current_user['id']
                                else None)

    # TODO-2 SPLITUP create new endpoints for these instead
    if 'posts' in request['params']:
        data['posts'] = [deliver_post(post) for post in
                         list_posts({'user_id': user['id']}, db_conn)]
    if ('subjects' in request['params']
            and user['settings']['view_subjects'] == 'public'):
        data['subjects'] = [
            subject.deliver()  # MMM
            for subject in list_user_subjects_entity(
                user['id'],
                {},
                db_conn)]
    if ('follows' in request['params']
            and user['settings']['view_follows'] == 'public'):
        data['follows'] = [deliver_follow(follow) for follow in
                           list_follows({'user_id': user['id']}, db_conn)]
    if 'avatar' in request['params']:
        size = int(request['params']['avatar'])
        data['avatar'] = get_avatar(user['email'], size if size else None)

    return 200, data


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
        user = get_user({'email': request['params'].get('name')}, db_conn)
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
