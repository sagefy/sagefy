from odm.model import Model, Field
from odm.validations import is_required, is_language, is_string


class Topic(Model):
    """A discussion topic."""
    tablename = 'topics'

    language = Field(
        validations=(is_required, is_language,),
        default='en'
    )
    entity_kind = Field(
        validations=(is_required, is_string,)
    )
    entity_id = Field(
        validations=(is_required, is_string,)
    )
    name = Field(
        validations=(is_required, is_string,)
    )
