from schemas.index import schema as default
from modules.util import extend


schema = extend({}, default, {
    'tablename': 'topics',
    'fields': {
        'user_id': {},
        'name': {},
        'entity_id': {  # TODO-1 validate foreign (circular)
        },
        'entity_kind': {},
    }
})
