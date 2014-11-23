"""
Routes for the discussion platform.
Includes topics, posts, proposals, votes, and flags.
"""

from flask import Blueprint, jsonify, request, abort
from models.discuss.proposal import Proposal
from flask.ext.login import current_user
from modules.util import parse_args
from modules.entity import get_latest_canonical, get_kind, create_entity
# from modules.discuss import get_post_facade, get_posts_facade, \
#     create_post_facade

topic = Blueprint('topic', __name__, url_prefix='/api/topics')


@topic.route('/', methods=['POST'])
def create_topic(topic_id):
    """
    Creates a new topic. The first post (proposal, flag) must be provided.
    Flag: if a flag for the same reason exists for the entity,
        create a vote there instead.
    """
    pass


@topic.route('/<topic_id>/', methods=['PUT', 'PATCH'])
def update_topic(topic_id):
    """
    Update the topic. Only the name can be changed. Only by original author.
    """
    pass


@topic.route('/<topic_id>/posts/', methods=['GET'])
def get_posts(topic_id):
    """
    Get a reverse chronological listing of posts for given topic.
    Includes topic meta data and posts (proposals, votes, flags).
    Paginates.
    """

    # TODO: update this endpoint to integrate
    # that this endpoint includes posts, proposals, votes, and flags.

    args = parse_args(request.args)

    # TODO: Pull up the proposal data

    # TODO: Pull up the proposal entity version

    # TODO: Pull up the proposal latest canonical version
    latest_canonical = get_latest_canonical(proposal.entity.kind,
                                            proposal.entity.entity_id)

    # TODO: If the proposal isn't based off the latest canonical, it's invalid

    # TODO: Make a diff between the latest canonical
    # ... and the proposal entity version

    # TODO: Return all the join proposal data to user

    pass


@topic.route('/<topic_id>/posts/', methods=['POST'])
def create_post(topic_id):
    """
    Create a new post on a given topic.
    Proposal: must include entity (card, unit, set) information.
    Vote: must refer to a proposal.
    """
    # TODO: Update to reflect that this endpoint creates
    # posts, proposals, votes, and flags

    if not current_user.is_authenticated():
        return abort(401)

    # Create a new entity version
    entity, errors = create_entity(request.json)

    if errors:
        return jsonify(errors=errors), 400

    # Create the proposal
    kind = get_kind(request.json)
    prop_data = request.json.proposal
    prop_data.entity = {
        'kind': kind,
        'entity_id': entity.entity_id,
        'id': entity.id
    }
    proposal, errors = Proposal.insert(prop_data)

    if errors:
        return jsonify(errors=errors), 400

    # Return the proposal and entity
    return jsonify(**{
        'proposal': proposal,
        kind: entity,
    })

    # VOTES:

    # TODO: outline function

    # TODO: If a proposal has sufficient votes, move it to canonical
    # ... and close out any prior versions dependent


@topic.route('/<topic_id>/posts/<post_id>/', methods=['PUT', 'PATCH'])
def update_post(topic_id, post_id):
    """
    Update an existing post. Must be one's own post.

    For proposals:
    The only field that can be updated is the status;
    the status can only be changed to declined, and only when
    the current status is pending or blocked.
    """
    if not current_user.is_authenticated():
        return abort(401)
    # TODO: outline function
