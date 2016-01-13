from framework.routes import get, post, delete, abort
from models.follow import Follow
from framework.session import get_current_user
from modules.entity import get_latest_accepted
from modules.entity import flush_entities
from models.topic import Topic


@get('/s/follows')
def get_follows_route(request):
    """
    Get a list of the users follows.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    follows = Follow.list(user_id=current_user['id'], **request['params'])

    output = {
        'follows': [follow.deliver(access='private') for follow in follows]
    }

    # TODO-3 SPLITUP should this be a different endpoint?
    if 'entities' in request['params']:
        entities = flush_entities(follow['entity'] for follow in follows)
        output['entities'] = [entity.deliver() if entity else None
                              for entity in entities]

    return 200, output


@post('/s/follows')
def follow_route(request):
    """
    Follow a card, unit, or set.
    """

    # TODO-3 simplify this method. does some of this belong in the model?

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    follow_data = dict(**request['params'])
    follow_data['user_id'] = current_user['id']

    follow = Follow(follow_data)
    errors = follow.validate()
    if errors:
        return 400, {
            'errors': errors,
            'ref': '4Qn9oWVWiGKvXSONQKHSy1T6'
        }

    # Ensure the entity exists   TODO-3 should this be a model validation?
    if follow['entity']['kind'] == 'topic':
        entity = Topic.get(id=follow['entity']['id'])
    else:
        entity = get_latest_accepted(follow['entity']['kind'],
                                     follow['entity']['id'])
    if not entity:
        return abort(404)

    follow, errors = follow.save()
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'gKU6wgTItxpKyDs0eAlonCmi',
        }

    return 200, {'follow': follow.deliver(access='private')}


@delete('/s/follows/{follow_id}')
def unfollow_route(request, follow_id):
    """
    Remove a follow. Must be current user's own follow.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    follow = Follow.get(id=follow_id)
    if not follow:
        return abort(404)

    if follow['user_id'] != current_user['id']:
        return abort(403)

    follow, errors = follow.delete()
    if errors:
        return 400, {
            'errors': errors,
            'ref': 'iGmpx8UwoFcKNmSKq9Aocy1a'
        }

    return 200, {}
