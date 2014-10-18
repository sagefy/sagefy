from odm.document import Document
from odm.model import Model, Field
from odm.embed import Embeds
from odm.validations import is_required, is_language, is_string


class TopicEntity(Document):
    kind = Field(
        validations=(is_required, is_string,)
    )
    entity_id = Field(
        validations=(is_required, is_string,)
    )


class Topic(Model):
    """A discussion topic."""
    tablename = 'topics'

    language = Field(
        validations=(is_required, is_language,),
        default='en'
    )
    name = Field(
        validations=(is_required, is_string,)
    )
    entity = Embeds(TopicEntity, validations=(is_required,))
