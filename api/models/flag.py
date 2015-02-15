from modules.model import Model
from models.post import Post
from modules.validations import is_required, is_one_of


class Flag(Post):
    """A proposal to delete a property."""

    schema = dict(Post.schema.copy(), **{
        'reason': {
            'validate': (is_required, (
                is_one_of, 'offensive', 'irrelevant', 'incorrect',
                           'unpublished', 'duplicate', 'inaccessible'
            ))
        },
        'status': {
            'validate': (is_required, (
                is_one_of, 'pending', 'blocked', 'accepted', 'declined'
            )),
            'default': 'pending'
        }
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__(self, fields)
        self['kind'] = 'flag'

    def validate(self):
        errors = super().validate()
        if not errors:
            errors += self.is_unique_flag()
        return errors

    def is_unique_flag(self):
        """
        Only one flag per entity per reason is allowed.
        """
        return []
        # TODO
