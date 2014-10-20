from odm.model import Model, Field
from odm.validations import is_required, is_string, is_one_of
from models.discuss.post import Post


class Proposal(Post):
    """A proposal to change the discussed entity."""
    entity_version_id = Field(
        validations=(is_required, is_string,)
    )
    name = Field(
        validations=(is_required, is_string,)
    )
    status = Field(
        validations=(is_required, (
            is_one_of, 'pending', 'blocked', 'accepted', 'declined'
        )),
        default='pending'
    )
    action = Field(
        validations=(is_required, (is_one_of, 'create', 'update', 'delete')),
    )

    def __init__(self, fields=None):
        """

        """
        Model.__init__(self, fields)
        self.kind = 'proposal'
