from models.card import Card
from modules.validations import is_required, is_string, is_url


class EmbedCard(Card):
    schema = dict(Card.schema.copy(), **{
        'url': {
            'validate': (is_required, is_string, is_url),
        },
        'rubric': {
            'validate': (),  # TODO@
        }
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__(fields)
        self['kind'] = 'embed'
