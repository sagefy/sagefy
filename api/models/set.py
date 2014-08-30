from odm.model import Model, Field
from odm.validations import is_required, is_language, is_string, is_boolean, \
    is_list


class Set(Model):
    """
    A set is a collection of units and other sets.
    Sets can vary greatly in scale.
    A graph is automatically formed based on the units and sets specified.
    """
    tablename = 'sets'

    entity_id = Field(
        validations=(is_required, is_string,),
        default=uniqid
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
    set_ids = Field(
        validations=(is_list,),
        default=[]
    )
    unit_ids = Field(
        validations=(is_list,),
        default=[]
    )
