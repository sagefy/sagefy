"""
Facade functions for discussion models, in particular
for post (sub: proposal, vote, flag).
"""

from models.post import Post
from models.proposal import Proposal
from models.vote import Vote
from models.flag import Flag
from flask import g
from modules.util import omit


def instance(data):
    """
    Given data from the database, return an appropriate model instance
    based on the `kind` field.
    """

    if data['kind'] is 'post':
        return Post(data)
    if data['kind'] is 'proposal':
        return Proposal(data)
    if data['kind'] is 'vote':
        return Vote(data)
    if data['kind'] is 'flag':
        return Flag(data)


def get_post_facade(post_id):
    """
    Gets the post and the correct kind based on the `kind` field.
    """

    data = g.db.table('posts').get(post_id).run(g.db_conn)
    return instance(data)


def get_posts_facade(limit=10, skip=0, **params):
    """
    Get posts, and return an array where each
    post is the correct kind based on the `kind` field.
    """

    data = g.db.table('posts') \
            .filter(params) \
            .skip(skip) \
            .limit(limit) \
            .run(g.db_conn)
    return [instance(d) for d in data]


def create_post_facade(data):
    """
    Creates the correct kind of post based on the `kind` field.
    """

    data = omit(data, ('id', 'created', 'modified'))
    model = instance(data)
    return model.save()
