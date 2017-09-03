from schemas.index import schema as default
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'responses',
    'fields': {
        'user_id': {},
        'card_id': {},
        'unit_id': {},
        'response': {},
        'score': {},
        'learned': {},
    },
})
