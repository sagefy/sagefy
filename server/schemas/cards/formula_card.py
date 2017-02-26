# TODO-3 is this just an extension of the number card?
from modules.util import extend
from modules.validations import is_required, is_string, is_list, is_number, \
    is_string_or_number, is_boolean, has_min_length


def is_list_of_variables(vars):
    """
    TODO-3 Ensure the data provided is a list of variables, with
    corresponding information.
    """
    pass


card_schema = {}  # TODO-3 import card_schema

schema = extend({}, card_schema, {
    'fields': {
        'body': {  # Question field
            'validate': (is_required, is_string,)
        },
        'options': {  # Available answers
            'validate': (is_required, is_list, (has_min_length, 1)),
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
    }
})
