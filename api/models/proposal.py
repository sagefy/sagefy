from modules.model import Model
from modules.validations import is_required, is_string, is_one_of
from models.post import Post


class Proposal(Post):
    """A proposal to change the discussed entity."""

    schema = dict(Post.schema.copy(), **{
        'entity_version_id': {
            'validate': (is_required, is_string,)
        },
        'name': {
            'validate': (is_required, is_string,)
        },
        'status': {
            'validate': (is_required, (
                is_one_of, 'pending', 'blocked', 'accepted', 'declined'
            )),
            'default': 'pending'
        },
        'action': {
            'validate': (is_required, (
                is_one_of, 'create', 'update', 'delete')),
        }
    })

    def __init__(self, fields=None):
        """

        """
        Model.__init__(self, fields)
        self.kind = 'proposal'
