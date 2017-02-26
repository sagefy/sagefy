from modules.util import extend
from modules.validations import is_required, is_string, is_one_of

card_schema = {}  # TODO-3 import card_schema

schema = extend({}, card_schema, {
    'fields': {
        'site': {
            'validate': (is_required, is_string, (
                is_one_of, 'soundcloud'),),
        },
        'audio_id': {
            'validate': (is_required, is_string,),
        }
    }
})
