from flask import Blueprint, jsonify, request, abort
from models.follow import Follow
from flask.ext.login import current_user
from modules.util import parse_args
from modules.entity import get_latest_canonical


follow_routes = Blueprint('follow', __name__, url_prefix='/api/follows')


@follow_routes.route('/', methods=['GET'])
def get_follows():
    """
    Get a list of the users follows.
    """

    if not current_user.is_authenticated():
        return abort(401)

    args = parse_args(request.args)
    follows = Follow.list(user_id=current_user.get_id(), **args)
    return jsonify(follows=[follow.deliver(access='private')
                            for follow in follows])


@follow_routes.route('/', methods=['POST'])
def follow():
    """
    Follow a card, unit, or set.
    """

    if not current_user.is_authenticated():
        return abort(401)

    follow_data = dict(**request.json)
    follow_data['user_id'] = current_user.get_id()

    follow = Follow(follow_data)
    errors = follow.validate()
    if errors:
        return jsonify(errors=errors), 400

    # Ensure the entity exists   TODO should this be a model validation?
    entity = get_latest_canonical(follow['entity']['kind'],
                                  follow['entity']['id'])
    if not entity:
        return abort(404)

    # Ensure we don't already follow   TODO should this be a model validation?
    prev = Follow.list(user_id=current_user.get_id(),
                       entity_id=follow_data['entity']['id'])
    if prev:
        return abort(409)

    follow, errors = follow.save()
    if errors:
        return jsonify(errors=errors), 400

    return jsonify(follow=follow.deliver(access='private'))


@follow_routes.route('/<follow_id>/', methods=['DELETE'])
def unfollow(follow_id):
    """
    Remove a follow. Must be current user's own follow.
    """

    if not current_user.is_authenticated():
        return abort(401)

    follow = Follow.get(id=follow_id)
    if not follow:
        return abort(404)

    if follow['user_id'] != current_user.get_id():
        return abort(403)

    follow, errors = follow.delete()
    if errors:
        return jsonify(errors=errors), 400

    return '', 204
