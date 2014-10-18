from odm.model import Model, Field
from odm.validations import is_required, is_language, is_string, is_boolean, \
    is_list
from modules.util import uniqid


class Card(Model):
    """
    Cards are the smallest entity in the Sagefy data structure system.
    A card represents a single learner activity.
    A card could present information, ask the learner to answer a question,
    collaborate with a small group to tackle a challenge,
    or create other cards.
    """
    tablename = 'cards'

    """
    The model represents a **version** of a card, not a card itself.
    The `entity_id` attribute is what refers to a particular card.
    The `id` attribute refers to a specific version of the card.
    """
    entity_id = Field(
        validations=(is_required, is_string,),
        default=uniqid
    )
    language = Field(
        validations=(is_required, is_language,),
        default='en'
    )
    unit_id = Field(
        validations=(is_required, is_string,)
    )
    name = Field(
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
    prerequisite_ids = Field(
        validations=(is_list,),
        default=[]
    )
    kind = Field(
        validations=(is_required, is_string,)
    )
