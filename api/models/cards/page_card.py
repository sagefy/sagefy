from models.card import Card
from modules.validations import is_required, is_string


class PageCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {
            'validate': (is_required, is_string,)
        },
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__(self, fields)
        self['kind'] = 'page'
