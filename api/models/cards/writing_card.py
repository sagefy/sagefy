from models.card import Card
from modules.validations import is_required, is_string, is_number


class WritingCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {
            'validate': (is_required, is_string,)
        },
        'max_characters': {
            'validate': (is_required, is_number,),
            'default': 0,
        },
        'rubric': {
            'validate': (),  # TODO@
        }
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__(fields)
        self['kind'] = 'writing'
