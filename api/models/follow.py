from odm.model import Model, Field
from odm.validations import is_required, is_string


class Follow(Model):
    """A following of an entity, topic, or proposal."""
    tablename = 'follows'

    user_id = Field(
        validations=(is_required, is_string,)
    )
    entity_kind = Field(
        validations=(is_required, is_string,)
    )
    entity_id = Field(
        validations=(is_required, is_string,)
    )
