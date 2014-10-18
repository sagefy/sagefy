from odm.document import Document
from odm.model import Model, Field
from odm.embed import Embeds
from odm.validations import is_required, is_language, is_string, is_one_of


class ProposalEntity(Document):
    """Summary information about the related entity."""
    kind = Field(
        validations=(is_required, is_string,
                     (is_one_of, 'card', 'unit', 'set'))
    )
    entity_id = Field(
        validations=(is_required, is_string,)
    )
    id = Field(  # `id` refers to version
        validations=(is_required, is_string,)
    )


class Proposal(Model):
    """A discussion topic."""
    tablename = 'proposals'

    language = Field(
        validations=(is_required, is_language,),
        default='en'
    )
    user_id = Field(
        validations=(is_required, is_string,)
    )
    name = Field(
        validations=(is_required, is_string,)
    )
    kind = Field(
        validations=(is_required, (is_one_of, 'create', 'update', 'delete')),
    )
    status = Field(
        validations=(is_required, (
            is_one_of, 'pending', 'blocked', 'accepted', 'declined'
        ))
    )
    entity = Embeds(ProposalEntity, validations=(is_required,))
