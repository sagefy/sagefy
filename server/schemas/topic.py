from schemas.index import schema as default
from modules.util import extend
from modules.validations import is_required, is_uuid, is_string, is_one_of


schema = extend({}, default, {
  'tablename': 'topics',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'name': {
      'validate': (is_required, is_string),
    },
    'entity_id': {
      'validate': (is_required, is_uuid,),
    },
    'entity_kind': {
      'validate': (is_required, is_string, (is_one_of, 'card', 'unit', 'subject')),
    },
  }
})
