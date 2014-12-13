from odm.model import Model, Field
from odm.validations import is_required, is_language, is_string, is_boolean, \
    is_list
from modules.util import uniqid


class Unit(Model):
    """
    A unit is the medium size in the Sagefy data structure system.
    A unit represents a unit of learning activity.
    A unit is defined by a single goal (objective). See Bloom’s Taxonomy.
    A unit should represent a goal that is as small as possible
    without becoming systemically redundant.
    An example of a unit is a small learning lesson,
    which may contain about five to eight minutes of information and
    30-60 minutes of practice to gain proficiency.
    """
    tablename = 'units'

    """
    The model represents a **version** of a unit, not a unit itself.
    The `entity_id` attribute is what refers to a particular unit.
    The `id` attribute refers to a specific version of the unit.
    The `previous_id` attribute refers to the version based off.
    """
    entity_id = Field(
        validations=(is_required, is_string,),
        default=uniqid
    )
    previous_id = Field(
        validations=(is_string,),
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
    requires_ids = Field(
        validations=(is_list,),
        default=[]
    )

    # TODO: Ensure no require cycles form
