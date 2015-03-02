from flask import Blueprint, jsonify, request, abort
from models.follow2 import Follow
from flask.ext.login import current_user
from modules.util import parse_args


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

    # TODO validate entity exists, use entity module

    follow, errors = Follow.insert(follow_data)
    if errors:
        return jsonify(errors=errors), 400

    return jsonify(follow=follow.deliver())


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
