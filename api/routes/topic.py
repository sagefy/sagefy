"""
Routes for the discussion platform.
Includes topics, posts, proposals, votes, and flags.
"""

from flask import Blueprint  # , jsonify, request, abort
# from models.proposal import Proposal
# from flask.ext.login import current_user
# from modules.util import parse_args
# from modules.entity import get_latest_canonical, get_kind, create_entity
# from modules.discuss import get_post_facade, get_posts_facade, \
#     create_post_facade

topic = Blueprint('topic', __name__, url_prefix='/api/topics')


@topic.route('/', methods=['POST'])
def create_topic(topic_id):
    """
    Create a new topic. The first post (proposal, flag) must be provided.
    Flag: if a flag for the same reason exists for the entity,
        create a vote there instead.
    """

    # TODO First, let's create the topic, but not save it

    # TODO Then, we'll create the post with the topic ID

    # TODO If errors, report back to user

    # TODO If both validate, then save both to the database

    # TODO Finally, report new URL to user


@topic.route('/<topic_id>/', methods=['PUT', 'PATCH'])
def update_topic(topic_id):
    """
    Update the topic. Only the name can be changed. Only by original author.
    """

    # TODO Must be logged in

    # TODO Request must only be for name

    # TODO Must be logged in as topic's author

    # TODO Update and notify user


@topic.route('/<topic_id>/posts/', methods=['GET'])
def get_posts(topic_id):
    """
    Get a reverse chronological listing of posts for given topic.
    Includes topic meta data and posts (proposals, votes, flags).
    Paginates.
    """

    # args = parse_args(request.args)

    # TODO Is the topic valid?

    # TODO Pull all kinds of posts

    # TODO For proposals, pull up the proposal entity version

    # TODO ...then pull up the proposal latest canonical version

    # TODO ...if the proposal isn't based off the latest canonical,
    #       it's invalid

    # TODO Make a diff between the latest canonical
    #       ... and the proposal entity version

    # TODO Return all data to user


@topic.route('/<topic_id>/posts/', methods=['POST'])
def create_post(topic_id):
    """
    Create a new post on a given topic.
    Accounts for posts, proposals, votes, and flags.
    Proposal: must include entity (card, unit, set) information.
    Vote: must refer to a proposal.
    """

    # TODO The user must be logged in

    # TODO For proposal or flag, entity must be included and valid

    # TODO For vote, must refer to a valid proposal

    # TODO The topic must be valid

    # TODO Try to save the post (and others)

    # TODO If error, show to user

    # TODO If a proposal has sufficient votes, move it to canonical
    #      ... and close out any prior versions dependent

    # TODO Give user new URL


@topic.route('/<topic_id>/posts/<post_id>/', methods=['PUT', 'PATCH'])
def update_post(topic_id, post_id):
    """
    Update an existing post. Must be one's own post.

    For proposals:
    The only field that can be updated is the status;
    the status can only be changed to declined, and only when
    the current status is pending or blocked.
    """

    # TODO A user must be logged in

    # TODO Must be user's own post

    # TODO If proposal, make sure its allowed changes

    # TODO Attempt to update

    # TODO If errors, report

    # TODO Notify user of success
