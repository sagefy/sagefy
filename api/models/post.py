from modules.model import Model
from modules.validations import is_required, is_string, is_one_of


def is_valid_kind(value):
    """
    Must belong to the same topic
    - TODO A post can reply to a post.
    - TODO A proposal can reply to post, proposal, or flag.
    - TODO A vote can reply to a proposal or flag.
    - TODO A flag cannot be a reply.
    """
    # TODO


class Post(Model):
    """A discussion post."""
    tablename = 'posts'

    schema = dict(Model.schema.copy(), **{
        'user_id': {
            'validate': (is_required, is_string,)
        },
        'topic_id': {
            'validate': (is_required, is_string,)
        },
        'body': {
            'validate': (is_required, is_string,)
        },
        'kind': {
            'validate': (is_required, is_string,
                         (is_one_of, 'post', 'proposal', 'vote', 'flag')),
            'default': 'post'
        },
        'replies_to_id': {
            'validate': (is_string, is_valid_kind)
        }
    })

    # TODO On create or update, index in Elasticsearch
