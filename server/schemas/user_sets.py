from schemas.index import schema as default
from modules.validations import is_required, is_string, is_list_of_strings
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'users_sets',
    'fields': {
        'user_id': {  # TODO-2 validate foreign
            'validate': (is_required, is_string,),
        },
        'set_ids': {
            'validate': (is_required, is_list_of_strings,),
        },
    }
})
