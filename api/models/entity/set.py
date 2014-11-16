from odm.document import Document
from odm.model import Model, Field
from odm.validations import is_required, is_language, is_string, is_boolean, \
    is_list, is_string_or_none, is_one_of
from odm.embed import EmbedsMany
from modules.util import uniqid


class SetEntity(Document):
    kind = Field(
        validations=(is_required, is_string, (
            is_one_of, 'unit', 'set',
        ))
    )
    entity_id = Field(
        validations=(is_required, is_string,)
    )


class Set(Model):
    """
    A set is a collection of units and other sets.
    Sets can vary greatly in scale.
    A graph is automatically formed based on the units and sets specified.
    """
    tablename = 'sets'

    """
    The model represents a **version** of a set, not a set itself.
    The `entity_id` attribute is what refers to a particular set.
    The `id` attribute refers to a specific version of the set.
    The `previous_id` attribute refers to the version based off.
    """
    entity_id = Field(
        validations=(is_required, is_string,),
        default=uniqid
    )
    previous_id = Field(
        validations=(is_string_or_none,),
    )
    language = Field(
        validations=(is_required, is_language,),
        default='en'
    )
    name = Field(
        validations=(is_required, is_string,)
    )
    body = Field(
        validations=(is_required, is_string,)
    )
    canonical = Field(
        validations=(is_boolean,),
        default=False
    )
    tags = Field(
        validations=(is_list,),
        default=[]
    )

    # TODO: Ensure no cycles form in `set_ids`
    entities = EmbedsMany(SetEntity, validations=(is_required,))
