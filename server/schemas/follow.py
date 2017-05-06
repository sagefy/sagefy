from modules.validations import is_required, is_string, is_one_of
from schemas.index import schema as default
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'follows',
    'fields': {
        'user_id': {  # TODO-2 validate foreign
            'validate': (is_required, is_string,)
        },
        'entity': {
            'validate': (is_required,),
            'embed': {
                'id': {
                    'validate': (is_required, is_string,),
                },
                'kind': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'card', 'unit', 'subject', 'topic'
                    )),
                }
            }
        }
    }
})
