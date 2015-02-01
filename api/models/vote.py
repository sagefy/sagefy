from modules.model import Model
from models.post import Post
from modules.validations import is_required, is_string, is_one_of


def is_unique_vote(instance):
    """
    Ensure a user can only vote once per proposal.
    """
    # TODO


class Vote(Post):
    """A vote or response on a proposal."""

    # For votes, a body is not required but optional,
    # But a replies to id is required
    schema = dict(Post.schema.copy(), **{
        # A vote does not require a body
        'body': {
            'validate': (is_string,)
        },

        # But a vote does require a proposal
        'replies_to_id': {
            'validate': (is_required, is_string,)
        },

        # The only true unique field of a vote...
        # Where True is yes, None is discuss, False is no
        'response': {
            'validate': ((is_one_of, True, None, False),),
            'default': None
        }
    })

    validations = (
        ('is unique vote', is_unique_vote),
    )

    def __init__(self, fields=None):
        """
        When creating a new vote,
        set the correct kind.
        """

        Model.__init__(self, fields)
        self.kind = 'vote'
