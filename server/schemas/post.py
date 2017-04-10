from schemas.index import schema as default
from modules.validations import is_required, is_string, is_one_of, \
    has_min_length
from modules.util import extend


schema = extend({}, default, {
    'tablename': 'posts',
    'fields': {
        'user_id': {  # TODO-2 validate foreign
            'validate': (is_required, is_string,)
        },
        'topic_id': {
            'validate': (is_required, is_string,)
        },
        'body': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
        'kind': {
            'validate': (is_required, is_string,
                         (is_one_of, 'post', 'proposal', 'vote')),
            'default': 'post'
        },
        'replies_to_id': {
            'validate': (is_string,)
        }
    },
})
