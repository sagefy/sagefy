"""
Facade functions for discussion models, in particular
for post (proposal, vote).
"""

from models.post import Post
from models.proposal import Proposal
from models.vote import Vote
import framework.database as database
from modules.util import omit
import rethinkdb as r


def instance(data):
    """
    Given data from the database, return an appropriate model instance
    based on the `kind` field.
    """

    if data.get('kind') == 'proposal':
        return Proposal(data)
    if data.get('kind') == 'vote':
        return Vote(data)

    return Post(data)


def get_post_facade(post_id):
    """
    Get the post and the correct kind based on the `kind` field.
    """

    data = Post.table.get(post_id).run(database.db_conn)
    return instance(data)


def get_posts_facade(limit=10, skip=0, **params):
    """
    Get posts, and return an array where each
    post is the correct kind based on the `kind` field.
    """

    data = (Post.table
                .filter(params)
                .order_by(r.asc('created'))
                .skip(skip)
                .limit(limit)
                .run(database.db_conn))
    return [instance(d) for d in data]


def create_post_facade(data):
    """
    Create the correct kind of post based on the `kind` field.
    """

    data = omit(data, ('id', 'created', 'modified'))
    model = instance(data)
    return model.save()


def instance_post_facade(data):
    """
    Create the correct kind of post based on the `kind` field.
    """

    data = omit(data, ('id', 'created', 'modified'))
    return instance(data)
