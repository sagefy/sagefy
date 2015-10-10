from models.card import Card
from modules.validations import is_required, is_string, is_number, is_list, \
    is_boolean, has_min_length


class NumberCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {  # Question field
            'validate': (is_required, is_string,),
        },
        'options': {
            'validate': (is_required, is_list, (has_min_length, 1)),
            'embed_many': {
                'value': {
                    'validate': (is_required, is_number,),
                },
                'correct': {
                    'validate': (is_required, is_boolean,),
                    'access': ('view',),
                },
                'feedback': {
                    'validate': (is_required, is_string,),
                    'access': ('view',),
                },
            }
        },
        'range': {
            'validate': (is_required, is_number,),
            'default': 0.001,
        },
        'default_incorrect_feedback': {
            'validate': (is_required, is_string,),
            'access': ('view',),
        },
    })

    def __init__(self, fields=None):
        """
        Create a new number card instance.
        """

        super().__init__(fields)
        self['kind'] = 'number'

    # TODO validate has_correct_options

    def validate_response(self, body):
        """
        TODO Ensure the given response body is valid,
        given the card information.
        """

        return []

    def score_response(self, response):
        """
        TODO Score the given response.
        Returns the score and feedback.
        """

        return 1, ''
