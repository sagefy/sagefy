from odm.model import Model, Field
from odm.validations import is_required, is_string, is_language


class Post(Model):
    """A discussion post."""
    tablename = 'posts'

    language = Field(
        validations=(is_required, is_language,),
        default='en'
    )
    user_id = Field(
        validations=(is_required, is_string,)
    )
    topic_id = Field(
        validations=(is_required, is_string,)
    )
    body = Field(
        validations=(is_required, is_string,)
    )
