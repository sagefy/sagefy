from modules.util import extend
from modules.validations import is_required, is_string, is_list, \
    is_list_of_strings, has_max_length, is_integer

media = (
    'document',
    'audio',
    'image',
    'video'
)

card_schema = {}  # TODO-3 import card_schema

schema = extend({}, card_schema, {
    'fields': {
        'body': {  # Question field
            'validate': (is_required, is_string,)
        },
        'file_extensions': {
            'validate': (is_required, is_list, is_list_of_strings,),
        },
        # TODO-3 What extensions are allowed? For what kind of media?
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
    }
})
