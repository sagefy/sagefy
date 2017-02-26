from schemas.index import schema as default
from modules.validations import is_required, is_string, is_number
from modules.util import extend
from modules.content import get as c


def is_score(val):
    if val > 1 or val < 0:
        return c('number')


schema = extend({}, default, {
    'tablename': 'responses',
    'fields': {
        'user_id': {
            'validate': (is_required, is_string,),
        },
        'card_id': {
            'validate': (is_required, is_string,),
        },
        'unit_id': {
            'validate': (is_required, is_string,),
        },
        'response': {
            'validate': (is_required,)
        },
        'score': {
            'validate': (is_required, is_number, is_score,),
        },
        'learned': {
            'validate': (is_required, is_number,)
        }
    }
})
