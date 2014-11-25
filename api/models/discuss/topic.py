from odm.document import Document
from odm.model import Model, Field
from odm.embed import Embeds
from odm.validations import is_required, is_string


class TopicEntity(Document):
    """Summary information about the related entity."""
    kind = Field(
        validations=(is_required, is_string,)
    )
    entity_id = Field(
        validations=(is_required, is_string,)
    )


class Topic(Model):
    """A discussion topic."""
    tablename = 'topics'

    user_id = Field(
        validations=(is_required, is_string,)
    )
    name = Field(
        validations=(is_required, is_string,)
    )
    entity = Embeds(TopicEntity, validations=(is_required,))

    # A topic must be created along with a post. No topic should have no posts.
