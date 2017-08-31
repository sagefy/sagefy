from schemas.index import schema as default
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'cards_parameters',
    'fields': {
        'entity_id': {},
        'guess_distribution': {},
        'slip_distribution': {},
    },
})
