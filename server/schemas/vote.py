from schemas.post import schema as post_schema
from modules.util import extend

schema = extend({}, post_schema, {
    'fields': {
        'response': {}
    },
})
