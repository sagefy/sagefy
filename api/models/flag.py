from odm.document import Document
from odm.model import Model, Field
from odm.embed import Embeds
from odm.validations import is_required, is_string, is_one_of


class FlagEntity(Document):
    entity_id = Field(
        validations=(is_required, is_string,)
    )
    kind = Field(
        validations=(is_required, is_string,)
    )


class Flag(Model):
    """A flag of an entity, post, or vote."""
    tablename = 'flags'

    user_id = Field(
        validations=(is_required, is_string,)
    )
    kind = Field(
        validations=(is_required, (
            is_one_of, 'offensive', 'irrelevant', 'incorrect',
                       'unpublished', 'duplicate', 'inaccessible'
        ))
    )
    entity = Embeds(FlagEntity, validations=(is_required,))
