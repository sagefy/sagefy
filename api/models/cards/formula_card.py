from models.card import Card
from modules.validations import is_required, is_string, is_list, is_number, \
    is_string_or_number, is_boolean


def is_list_of_variables(vars):
    """
    TODO@ Ensure the data provided is a list of variables, with
    corresponding information.
    """
    pass


class FormulaCard(Card):
    schema = dict(Card.schema.copy(), **{
        'body': {  # Question field
            'validate': (is_required, is_string,)
        },
        'options': {  # Available answers
            'validate': (is_required, is_list,),
            'embed_many': {
                'value': {
                    'validate': (is_required, is_string_or_number,),
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
        'variables': {
            'validate': (is_required, is_list, is_list_of_variables,),
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
        Create a new formula card instance.
        """

        super().__init__(fields)
        self['kind'] = 'formula'

    # TODO@ validate has_correct_options

    def is_valid_response(self, body):
        """
        @TODO Ensure the given response body is valid,
        given the card information.
        """

        return []
