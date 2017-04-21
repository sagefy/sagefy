from schemas.post import schema as post_schema
from modules.validations import is_required, is_string, is_one_of, is_dict
from modules.util import extend


schema = extend({}, post_schema, {
    'fields': {
        'entity_versions': {
            'validate': (is_required, is_dict,),
            'embed_many': {
                'id': {
                    'validate': (is_required, is_string,),
                },
                'kind': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'card', 'unit', 'set',
                    )),
                }
            }
        },
        'name': {
            'validate': (is_required, is_string,)
        },
    },
})
