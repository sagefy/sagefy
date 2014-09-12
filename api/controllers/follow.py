from flask import Blueprint, jsonify, request
from models.follow import Follow
from flask.ext.login import current_user

follow = Blueprint('follow', __name__, url_prefix='/api/follows')


@follow.route('/', methods=['POST'])
def follow():
    """
    Current user follows an entity, topic, or proposal.
    """
    pass


@follow.route('/<follow_id>', methods=['DELETE'])
def unfollow():
    """
    Remove a follow. Must be current user's own follow.
    """
    pass
