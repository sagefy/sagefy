from schemas.index import schema as default
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'users_subjects',
    'fields': {
        'user_id': {
        },
        'subject_ids': {
        },
    }
})
