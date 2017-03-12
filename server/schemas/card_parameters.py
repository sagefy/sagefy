from modules.validations import is_required, is_string, is_dict
from schemas.index import schema as default
from modules.util import extend

schema = extend({}, default, {
    'tablename': 'cards_parameters',
    'fields': {
        'entity_id': {  # TODO-3 validate foreign
            'validate': (is_required, is_string),
        },
        'guess_distribution': {
            'validate': (is_required, is_dict,),
        },
        'slip_distribution': {
            'validate': (is_required, is_dict,),
        },
    },
})
