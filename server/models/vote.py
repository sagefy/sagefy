from models.post import Post
from modules.validations import is_required, is_string, is_boolean


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
        },   # TODO-1 Validate this is for a valid proposal

        # The only true unique field of a vote...
        # Where True is yes, False is no
        'response': {
            'validate': (is_boolean,),
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
        TODO-1 Ensure a user can only vote once per proposal.
        """
        return []

    def is_valid_reply_kind(self):
        """
        TODO-1 A vote can reply to a proposal.
        TODO-1 A vote cannot reply to a proposal that is accepted or declined.
        """
        return []
