from schemas.index import schema as default
from modules.util import extend


schema = extend({}, default, {
    'tablename': 'posts',
    'fields': {
        'user_id': {},
        'topic_id': {},
        'body': {},
        'kind': {},
        'replies_to_id': {},
    },
})
