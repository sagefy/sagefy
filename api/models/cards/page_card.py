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
        Create a new page card instance.
        """

        super().__init__(fields)
        self['kind'] = 'page'

    def validate_response(self, body):
        """
        Ensure the given response body is valid, given the card information.
        """

        return [{'message': 'No response is valid.'}]
