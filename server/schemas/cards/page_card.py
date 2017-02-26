from modules.util import extend
from modules.validations import is_required, is_string

card_schema = {}  # TODO-3 import card_schema

schema = extend({}, card_schema, {
    'fields': {
        'body': {
            'validate': (is_required, is_string,)
        },
    }
})
