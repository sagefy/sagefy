from schemas.index import schema as default
from modules.validations import is_required, is_string, is_one_of, \
    has_min_length
from modules.util import extend


schema = extend({}, default, {
    'tablename': 'topics',
    'fields': {
        'user_id': {  # TODO-2 validate foreign
            'validate': (is_required, is_string,)
        },
        'name': {
            'validate': (is_required, is_string, (has_min_length, 1),)
        },
        'entity': {
            'validate': (is_required,),
            'embed': {
                'id': {  # TODO-1 validate foreign (circular)
                    'validate': (is_required, is_string,),
                },
                'kind': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'card', 'unit', 'subject'
                    )),
                }
            }
        }
    }
})
