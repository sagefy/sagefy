from modules.model import Model
from modules.validations import is_required, is_language, is_string, \
    is_boolean, is_list, is_one_of
from modules.util import uniqid


class SetEntity(Document):
    kind = Field(
        validate=(is_required, is_string, (
            is_one_of, 'unit', 'set',
        ))
    )
    entity_id = Field(
        validate=(is_required, is_string,)
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
        validate=(is_required, is_string,),
        default=uniqid
    )
    previous_id = Field(
        validate=(is_string,),
    )
    language = Field(
        validate=(is_required, is_language,),
        default='en'
    )
    name = Field(
        validate=(is_required, is_string,)
    )
    body = Field(
        validate=(is_required, is_string,)
    )
    canonical = Field(
        validate=(is_boolean,),
        default=False
    )
    tags = Field(
        validate=(is_list,),
        default=[]
    )

    # TODO: Ensure no cycles form in `set_ids`
    members = EmbedsMany(SetEntity, validate=(is_required,))
