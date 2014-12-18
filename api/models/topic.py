from modules.model import Model
from modules.validations import is_required, is_string


class TopicEntity(Document):
    """Summary information about the related entity."""
    kind = Field(
        validate=(is_required, is_string,)
    )
    entity_id = Field(
        validate=(is_required, is_string,)
    )


class Topic(Model):
    """A discussion topic."""
    tablename = 'topics'

    user_id = Field(
        validate=(is_required, is_string,)
    )
    name = Field(
        validate=(is_required, is_string,)
    )
    entity = Embeds(TopicEntity, validate=(is_required,))

    # A topic must be created along with a post. No topic should have no posts.
