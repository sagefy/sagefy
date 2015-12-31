from modules.validations import is_required, is_string, is_one_of, is_dict
from models.post import Post


class Proposal(Post):
    """A proposal to change the discussed entity."""

    schema = dict(Post.schema.copy(), **{
        'entity_version': {
            'validate': (is_required, is_dict,),
            'embed': {
                'id': {  # TODO-1 is valid ids?
                    'validate': (is_required, is_string,),
                },
                'kind': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'card', 'unit', 'set',
                    )),
                }
            }
        },
        'name': {
            'validate': (is_required, is_string,)
        },
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__(fields)
        self.kind = 'proposal'

    def validate(self):
        errors = super().validate()
        if not errors:
            errors += self.is_valid_reply_kind()
        if not errors:
            errors += self.is_valid_version()
        return errors

    def is_valid_reply_kind(self):
        """
        TODO-1 A proposal can reply to post or proposal.
        """
        return []

    def is_valid_version(self):
        """
        TODO-1 Ensure this is a valid version of the entity.
        """
        return []
