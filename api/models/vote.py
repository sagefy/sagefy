from models.post import Post
from modules.validations import is_required, is_string, is_one_of


class Vote(Post):
    """
    A vote or response on a proposal.
    """

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

    def __init__(self, fields=None):
        """
        When creating a new vote,
        set the correct kiwnd.
        """

        super().__init__(fields)
        self.kind = 'vote'

    def validate(self):
        errors = super().validate()
        if not errors:
            errors += self.is_unique_vote()
        if not errors:
            errors += self.is_valid_reply_kind()
        return errors

    def is_unique_vote(self):
        """
        TODO@ Ensure a user can only vote once per proposal.
        """
        return []

    def is_valid_reply_kind(self):
        """
        - TODO@ A vote can reply to a proposal or flag.
        """
        return []
