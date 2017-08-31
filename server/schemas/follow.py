from schemas.index import schema as default
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'follows',
    'fields': {
        'user_id': {},
        'entity_id': {},
        'entity_kind': {},
    }
})
