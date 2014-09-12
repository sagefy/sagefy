from odm.model import Model, Field
from odm.validations import is_required, is_string, is_language


class Vote(Model):
    """A vote or response on a proposal."""
    tablename = 'votes'

    language = Field(
        validations=(is_required, is_language,),
        default='en'
    )
    user_id = Field(
        validations=(is_required, is_string,)
    )
    proposal_id = Field(
        validations=(is_required, is_string,)
    )
    body = Field(
        validations=(is_required, is_string,)
    )
    kind = Field(
        validations=((is_one_of, True, None, False),),
        default=None
    )  # Where True is yes, None is discuss, False is no
