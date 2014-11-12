from odm.model import Model
from odm.field import Field
from models.discuss.post import Post
from odm.validations import is_required, is_string, is_one_of


class Vote(Post):
    """A vote or response on a proposal."""
    proposal_id = Field(
        validations=(is_required, is_string,)
    )
    response = Field(
        validations=((is_one_of, True, None, False),),
        default=None
    )  # Where True is yes, None is discuss, False is no

    def __init__(self, fields=None):
        """

        """
        Model.__init__(self, fields)
        self.kind = 'vote'

    # You can only vote once per proposal.
    # You can update the response on your vote.
    # You cannot vote on your own proposal.
    # A vote should not require a body.
