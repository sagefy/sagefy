from models.user_sets import UserSets
from models.set import Set
from framework.routes import get, post, put, delete, abort
from framework.session import get_current_user


@get('/s/users/{user_id}/sets')
def get_user_sets_route(request, user_id):
    """
    Get the list of sets the user has added.

    NEXT STATE
    GET Choose Set
        -> POST Choose Set
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    if user_id != current_user['id']:
        return abort(403)

    next_ = {
        'method': 'POST',
        'path': '/s/users/{user_id}/sets/{set_id}'
                .format(user_id=current_user['id'],
                        set_id='{set_id}'),
    }
    current_user.set_learning_context(next=next_)

    uset = UserSets.get(user_id=user_id)
    if not uset:
        return 200, {'sets': [], 'next': next_}
    return 200, {
        'sets': [s.deliver() for s in uset.list_sets(**request['params'])],
        'next': next_,
    }


@post('/s/users/{user_id}/sets/{set_id}')
def add_set_route(request, user_id, set_id):
    """
    Add a set to the learner's list of sets.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    if user_id != current_user['id']:
        return abort(403)

    set_ = Set.get(entity_id=set_id)
    if not set_:
        return abort(404)

    uset = UserSets.get(user_id=user_id)
    if uset and set_id in uset['set_ids']:
        return 400, {
            'errors': [{
                'name': 'set_id',
                'message': 'Set is already added.',
            }],
            'ref': 'kPZ95zM3oxFDGGl8vBdR3J3o',
        }

    if uset:
        uset['set_ids'].append(set_id)
        uset, errors = uset.save()
    else:
        uset, errors = UserSets.insert({
            'user_id': user_id,
            'set_ids': [set_id],
        })

    if errors:
        return 400, {
            'errors': errors,
            'ref': 'zCFUbLBTg9n2DnTkQYbqO4X9'
        }

    return 200, {'sets': uset['set_ids']}


@put('/s/users/{user_id}/sets/{set_id}')
def select_set_route(request, user_id, set_id):
    """
    Select the set to work on.

    NEXT STATE
    POST Choose Set   (Update Learner Context)
        -> GET View Set Tree
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    set_ = Set.get_latest_accepted(set_id)
    next_ = {
        'method': 'GET',
        'path': '/s/sets/{set_id}/tree'
                .format(set_id=set_id),
    }
    current_user.set_learning_context(set=set_.data, next=next_)

    return 200, {'next': next_}


@delete('/s/users/{user_id}/sets/{set_id}')
def remove_set_route(request, user_id, set_id):
    """
    Remove a set from the learner's list of sets.
    """

    current_user = get_current_user(request)
    if not current_user:
        return abort(401)

    if user_id != current_user['id']:
        return abort(403)

    uset = UserSets.get(user_id=user_id)
    if not uset:
        return 404, {
            'errors': [{'message': 'User does not have sets.'}],
            'ref': '8huZbvEAYOP8LcZb2sXbqNOC'
        }

    if set_id not in uset['set_ids']:
        return abort(404)

    uset['set_ids'].remove(set_id)
    usets, errors = uset.save()

    if errors:
        return 400, {
            'errors': errors,
            'ref': 'qIfll1e7dbP9V9jmC8FkCwsa'
        }

    return 200, {'sets': uset['set_ids']}
