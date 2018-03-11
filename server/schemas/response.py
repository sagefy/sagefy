from schemas.index import schema as default
from modules.util import extend
from modules.validations import is_required, is_uuid, is_string, is_number, \
    is_in_range

schema = extend({}, default, {
  'tablename': 'responses',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'card_id': {
      'validate': (is_required, is_uuid,),
    },
    'unit_id': {
      'validate': (is_required, is_uuid,),
    },
    'response': {
      'validate': (is_required, is_string,),
    },
    'score': {
      'validate': (is_required, is_number, (is_in_range, 0, 1)),
    },
    'learned': {
      'validate': (is_required, is_number, (is_in_range, 0, 1)),
    },
  },
})
