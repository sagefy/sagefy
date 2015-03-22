from models.card import Card
from modules.validations import is_required, is_string, is_integer, is_list, \
    has_max_length


class WritingCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {
            'validate': (is_required, is_string,)
        },
        'max_characters': {
            'validate': (is_required, is_integer,),
            'default': 1000,
        },
        'rubric': {
            'validate': (is_required, is_list, (has_max_length, 5)),
            'embed_many': {
                'body': {
                    'validate': (is_required, is_string,),
                },
                'value': {
                    'validate': (is_required, is_integer,),
                    'default': 1,
                },
                'body_none': {  # Incomplete  (0%)
                    'validate': (is_required, is_string,),
                },
                'body_half': {  # Needs Work  (50%)
                    'validate': (is_required, is_string,),
                },
                'body_full': {  # Good  (100%)
                    'validate': (is_required, is_string,),
                },
            },
        },
    })

    def __init__(self, fields=None):
        """
        Create a new writing card instance.
        """

        super().__init__(fields)
        self['kind'] = 'writing'

    def validate_response(self, body):
        """
        @TODO Ensure the given response body is valid,
        given the card information.
        """

        return []
