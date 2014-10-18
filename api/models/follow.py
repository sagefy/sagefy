from odm.document import Document
from odm.model import Model, Field
from odm.embed import Embeds
from odm.validations import is_required, is_string


class FollowEntity(Document):
    kind = Field(
        validations=(is_required, is_string,)
    )
    entity_id = Field(
        validations=(is_required, is_string,)
    )


class Follow(Model):
    """A following of an entity, topic, or proposal."""
    tablename = 'follows'

    user_id = Field(
        validations=(is_required, is_string,)
    )
    entity = Embeds(FollowEntity, validations=(is_required,))
