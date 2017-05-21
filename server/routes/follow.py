from framework.routes import get, post, delete, abort
from framework.session import get_current_user
from database.follow import get_follow, list_follows, insert_follow, \
    deliver_follow, delete_follow
from database.entity_base import get_latest_accepted
from database.entity_facade import deliver_entity_by_kind


@get('/s/follows')
def get_follows_route(request):
    """
    Get a list of the users follows.
    """

    db_conn = request['db_conn']

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    params = dict(**request['params'])
    params['user_id'] = current_user['id']

    follows = list_follows(params, db_conn)

    output = {
        'follows': [deliver_follow(follow, access='private')
                    for follow in follows]
    }

    # TODO-3 SPLITUP this be a different endpoint
    if 'entities' in request['params']:
        output['entities'] = []
        for follow in follows:
            entity_kind = follow['entity']['kind']
            entity_id = follow['entity']['id']
            tablename = '%ss' % entity_kind
            entity = get_latest_accepted(tablename, db_conn, entity_id)
            output['entities'].append(
                deliver_entity_by_kind(entity_kind, entity)
            )

    return 200, output


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
