from models.card import Card
from modules.validations import is_required, is_string, is_list, \
    is_list_of_strings

media = (
    'document',
    'audio',
    'image',
    'video'
)


class UploadCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {  # Question field
            'validate': (is_required, is_string,)
        },
        'file_extensions': {
            'validate': (is_required, is_list, is_list_of_strings,),
        },
        # TODO What extensions are allowed? For what kind of media?
        'rubric': {
            'validate': (),  # TODO
        }
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__()
        self['kind'] = 'upload'
