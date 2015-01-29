from flask import Blueprint, jsonify, request, abort
from models.follow import Follow
from flask.ext.login import current_user

follow = Blueprint('follow', __name__, url_prefix='/api/follows')


@follow.route('/', methods=['POST'])
def follow():
    """
    Follow a card, unit, or set.
    """

    if not current_user.is_authenticated():
        return abort(401)

    follow_data = dict(**request.body)
    follow_data['user_id'] = current_user.get_id()

    # TODO validate entity exists

    follow, errors = Follow.insert(follow_data)
    if errors:
        return jsonify(errors=errors), 400

    return jsonify(follow=follow.deliver())


@follow.route('/<follow_id>/', methods=['DELETE'])
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
