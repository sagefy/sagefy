from models.card import Card
from modules.validations import is_required, is_string, is_list, is_boolean


class MatchCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {  # Question field
            'validate': (is_required, is_string,)
        },
        'options': {  # Available answers
            'validate': (is_required, is_list,),
            'embed_many': {
                'value': {
                    'validate': (is_required, is_string,),
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
        'default_incorrect_feedback': {
            'validate': (is_required, is_string,),
            'access': ('view',),
        },
        'case_sensitive': {
            'validate': (is_boolean,),
            'default': False,
        }
    })

    def __init__(self, fields=None):
        """
        Create a new match card instance.
        """

        super().__init__(fields)
        self['kind'] = 'match'

    # TODO@ validate has_correct_options

    def is_valid_response(self, body):
        """
        @TODO Ensure the given response body is valid,
        given the card information.
        """

        return []
