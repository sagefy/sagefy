from modules.util import extend
from modules.validations import is_required, is_string, is_number, is_list, \
    is_boolean, has_min_length

card_schema = {}  # TODO-3 import card_schema

schema = extend({}, card_schema, {
    'fields': {
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
    }
})
