from models.user_sets import UserSets
from models.set import Set
from framework.index import get, post, delete, abort
from framework.session import get_current_user


@get('/api/users/{user_id}/sets')
def get_user_sets_route(request, user_id):
    """
    Get the list of sets the user has added.
    """

    current_user = get_current_user()
    if not current_user:
        return abort(401)

    if user_id != current_user['id']:
        return abort(403)

    uset = UserSets.get(user_id=user_id)
    if not uset:
        return 200, {'sets': []}
    return 200, {
        'sets': [s.deliver() for s in uset.list_sets(**request['params'])]
    }


@post('/api/users/{user_id}/sets/{set_id}')
def add_set_route(request, user_id, set_id):
    """
    Add a set to the learner's list of sets.
    """

    current_user = get_current_user()
    if not current_user:
        return abort(401)

    if user_id != current_user['id']:
        return abort(403)

    set_ = Set.get(entity_id=set_id)
    if not set_:
        return abort(404)

    uset = UserSets.get(user_id=user_id)
    if uset and set_id in uset['set_ids']:
        return 400, {'errors': [{
            'name': 'set_id',
            'message': 'Set is already added.',
        }]}

    if uset:
        uset['set_ids'].append(set_id)
        uset, errors = uset.save()
    else:
        uset, errors = UserSets.insert({
            'user_id': user_id,
            'set_ids': [set_id],
        })

    if errors:
        return 400, {'errors': errors}

    return 200, {'sets': uset['set_ids']}


@delete('/api/users/{user_id}/sets/{set_id}')
def remove_set_route(request, user_id, set_id):
    """
    Remove a set from the learner's list of sets.
    """

    current_user = get_current_user()
    if not current_user:
        return abort(401)

    if user_id != current_user['id']:
        return abort(403)

    uset = UserSets.get(user_id=user_id)
    if not uset or set_id not in uset['set_ids']:
        return abort(404)

    uset['set_ids'].remove(set_id)
    usets, errors = uset.save()

    if errors:
        return 400, {'errors': errors}

    return 200, {'sets': uset['set_ids']}
