from models.user_sets import UserSets
from models.set import Set
from modules.util import parse_args
from flask import Blueprint, abort, request, jsonify
from flask.ext.login import current_user


user_sets_routes = Blueprint('user_sets', __name__,
                             url_prefix='/api/users')


@user_sets_routes.route('/<user_id>/sets/', methods=['GET'])
def get_user_sets(user_id):
    """
    Get the list of sets the user has added.
    """

    if not current_user.is_authenticated():
        return abort(401)

    if user_id != current_user.get_id():
        return abort(403)

    args = parse_args(request.args)
    uset = UserSets.get(user_id=user_id)
    if not uset:
        return jsonify(sets=[])
    return jsonify(sets=uset.list_sets(**args))


@user_sets_routes.route('/<user_id>/sets/<set_id>/', methods=['POST'])
def add_set(user_id, set_id):
    """
    Add a set to the learner's list of sets.
    """

    if not current_user.is_authenticated():
        return abort(401)

    if user_id != current_user.get_id():
        return abort(403)

    set_ = Set.get(entity_id=set_id)
    if not set_:
        return abort(404)

    uset = UserSets.get(user_id=user_id)
    if uset and set_id in uset['set_ids']:
        return jsonify(errors=[{
            'name': 'set_id',
            'message': 'Set is already added.',
        }]), 400

    if uset:
        uset['set_ids'].append(set_id)
        uset, errors = uset.save()
    else:
        uset, errors = uset.insert({
            'user_id': user_id,
            'set_ids': [set_id],
        })

    if errors:
        return jsonify(errors=errors), 400
    return jsonify(sets=uset['set_ids'])


@user_sets_routes.route('/<user_id>/sets/<set_id>/', methods=['DELETE'])
def remove_set(user_id, set_id):
    """
    Remove a set from the learner's list of sets.
    """

    if not current_user.is_authenticated():
        return abort(401)

    if user_id != current_user.get_id():
        return abort(403)

    uset = UserSets.get(user_id=user_id)
    if not uset or set_id not in uset['set_ids']:
        return abort(404)

    uset['set_ids'].remove(set_id)
    usets, errors = uset.save()

    if errors:
        return jsonify(errors=errors), 400
    return jsonify(sets=uset['set_ids'])
