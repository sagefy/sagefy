from modules.model import Model
from modules.validations import is_required, is_string, is_one_of


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

        # Must belong to the same topic
        # a post can reply to a post, proposal, flag, or vote
        # a proposal can reply to post, proposal, or flag
        # a vote can reply to a proposal or flag
        # a flag cannot be a reply
        'replies_to_id': {
            'validate': (is_string,)
        }
    })
