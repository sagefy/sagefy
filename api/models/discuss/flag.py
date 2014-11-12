from odm.model import Model
from odm.field import Field
from models.discuss.proposal import Proposal
from odm.validations import is_required, is_one_of


class Flag(Proposal):
    """A proposal to delete a property."""
    reason = Field(
        validations=(is_required, (
            is_one_of, 'offensive', 'irrelevant', 'incorrect',
                       'unpublished', 'duplicate', 'inaccessible'
        ))
    )

    def __init__(self, fields=None):
        """

        """
        Model.__init__(self, fields)
        self.kind = 'flag'
        self.action = 'delete'

    # Only one flag proposal per entity per reason is allowed.
    # Otherwise, its a vote for the existing flag proposal for that reason.
