from schemas.index import schema as default
from modules.util import extend


schema = extend({}, default, {
    'tablename': 'topics',
    'fields': {
        'user_id': {},
        'name': {},
        'entity_id': {},
        'entity_kind': {},
    }
})
