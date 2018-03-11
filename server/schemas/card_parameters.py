from schemas.index import schema as default
from modules.util import extend
from modules.validations import is_required, is_uuid, is_dict

schema = extend({}, default, {
  'tablename': 'cards_parameters',
  'fields': {
    'entity_id': {
      'validate': (is_required, is_uuid,)
    },
    'guess_distribution': {
      'validate': (is_required, is_dict,)
    },
    'slip_distribution': {
      'validate': (is_required, is_dict,)
    },
  },
})
