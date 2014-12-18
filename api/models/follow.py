from modules.model import Model, Field
from modules.validations import is_required, is_string


class FollowEntity(Document):
    kind = Field(
        validate=(is_required, is_string,)
    )
    entity_id = Field(
        validate=(is_required, is_string,)
    )


class Follow(Model):
    """A following of an entity, topic, or proposal."""
    tablename = 'follows'

    user_id = Field(
        validate=(is_required, is_string,)
    )
    entity = Embeds(FollowEntity, validate=(is_required,))
