import rethinkdb as r
from modules.util import uniqid


def update_modified(field):
    return r.now()


schema = {
    'tablename': '',
    'fields': {
        'id': {
            'default': uniqid
            # RethinkDB by default uses UUID, but as its JSON,
            # there's no reason to not use the full alphanumeric set
        },
        'created': {
            'default': r.now()
        },
        'modified': {
            'default': r.now(),
            'bundle': update_modified
        }
    },
    'validate': [],
}
