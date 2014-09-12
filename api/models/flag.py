from odm.model import Model, Field
from odm.validations import is_required, is_string, is_one_of


class Flag(Model):
    """A flag of an entity, post, or vote."""
    tablename = 'flags'

    user_id = Field(
        validations=(is_required, is_string,)
    )
    entity_kind = Field(
        validations=(is_required, is_string,)
    )
    entity_id = Field(
        validations=(is_required, is_string,)
    )
    kind = Field(
        validations=(is_required, (
            is_one_of, 'offensive', 'irrelevant', 'incorrect',
                       'unpublished', 'duplicate', 'inaccessible'
        ))
    )
