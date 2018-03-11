from schemas.index import schema as default
from modules.util import extend
from modules.validations import is_required, is_uuid


schema = extend({}, default, {
  'tablename': 'users_subjects',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'subject_id': {
      'validate': (is_required, is_uuid,),
    },
  },
})
