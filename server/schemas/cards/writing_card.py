from modules.util import extend
from modules.validations import is_required, is_string, is_integer, is_list, \
    has_max_length

card_schema = {}  # TODO-3 import card_schema

schema = extend({}, card_schema, {
    'fields': {
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
    },
})
