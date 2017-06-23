from framework.routes import get, post, delete, abort
from framework.session import get_current_user
from database.follow import get_follow, list_follows, insert_follow, \
    deliver_follow, delete_follow
from database.user import get_user


@get('/s/follows')
def get_follows_route(request):
    """
    Get a list of the users follows.
    """

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    user_id = request['params'].get('user_id')
    if user_id:
        user = get_user({'id': user_id}, db_conn)
        if not user:
            return abort(404)
        if (user != current_user and
                user['settings']['view_follows'] != 'public'):
            return abort(403)
    else:
        user = current_user
        if not user:
            return abort(401)
    params = dict(**request['params'])
    params['user_id'] = user['id']
    follows = list_follows(params, db_conn)
    return 200, {
        'follows': [deliver_follow(follow, access='private')
                    for follow in follows]
    }


@post('/s/follows')
def follow_route(request):
    """
    Follow a card, unit, or subject.
    """

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    follow_data = dict(**request['params'])
    follow_data['user_id'] = current_user['id']
    follow, errors = insert_follow(follow_data, db_conn)
    if errors:
        return 400, {
            'errors': errors,
            'ref': '4Qn9oWVWiGKvXSONQKHSy1T6'
        }
    return 200, {'follow': deliver_follow(follow, access='private')}


@delete('/s/follows/{follow_id}')
def unfollow_route(request, follow_id):
    """
    Remove a follow. Must be current user's own follow.
    """

    db_conn = request['db_conn']
    current_user = get_current_user(request)
    if not current_user:
        return abort(401)
    follow = get_follow({'id': follow_id}, db_conn)
    if not follow:
        return abort(404)
    if follow['user_id'] != current_user['id']:
        return abort(403)
    errors = delete_follow(follow['id'], db_conn)
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'iGmpx8UwoFcKNmSKq9Aocy1a'
        }
    return 200, {}
