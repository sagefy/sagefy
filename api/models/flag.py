from odm.model import Model
from odm.field import Field
from models.post import Post
from odm.validations import is_required, is_one_of


class Flag(Post):
    """A proposal to delete a property."""
    reason = Field(
        validations=(is_required, (
            is_one_of, 'offensive', 'irrelevant', 'incorrect',
                       'unpublished', 'duplicate', 'inaccessible'
        ))
    )
    status = Field(
        validations=(is_required, (
            is_one_of, 'pending', 'blocked', 'accepted', 'declined'
        )),
        default='pending'
    )

    def __init__(self, fields=None):
        """

        """
        Model.__init__(self, fields)
        self.kind = 'flag'

    # Only one flag per entity per reason is allowed.
    # Otherwise, its a vote for the existing flag proposal for that reason.
