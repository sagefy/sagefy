from odm.model import Model, Field
from odm.validations import is_required, is_string, is_one_of


class Post(Model):
    """A discussion post."""
    tablename = 'posts'

    user_id = Field(
        validations=(is_required, is_string,)
    )
    topic_id = Field(
        validations=(is_required, is_string,)
    )
    body = Field(
        validations=(is_required, is_string,)
    )
    kind = Field(
        validations=(is_required, is_string,
                     (is_one_of, 'post', 'proposal', 'vote', 'flag')),
        default='post'
    )
