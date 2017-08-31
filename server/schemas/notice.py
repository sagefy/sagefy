from schemas.index import schema as default
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'notices',
    'fields': {
        'user_id': {},
        'kind': {},
        'data': {
            'default': {},
        },
        'read': {},
        'tags': {},
    }
})
