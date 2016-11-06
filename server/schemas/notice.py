from schemas.index import schema as default
from modules.validations import is_required, is_string, is_boolean, is_list, \
    is_one_of, is_list_of_strings, is_dict
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'notices',
    'fields': {
        'user_id': {  # TODO-2 validate foreign
            'validate': (is_required, is_string,)
        },
        'kind': {
            'validate': (is_required, is_string, (
                is_one_of,
                'create_topic',
                'create_proposal',
                'block_proposal',
                'decline_proposal',
                'accept_proposal',
                'create_post',
                'come_back',
            ))
        },
        'data': {
            'validate': (is_dict,),
            'default': {},
        },
        'read': {
            'validate': (is_boolean,),
            'default': False
        },
        'tags': {
            'validate': (is_list, is_list_of_strings),
            'default': []
        }
    }
})
