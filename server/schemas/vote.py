from schemas.post import schema as post_schema
from modules.util import extend
from modules.validations import is_string, is_required, is_boolean, is_uuid

schema = extend({}, post_schema, {
  'fields': {
    'response': {
      'validate': (is_required, is_boolean,),
    }
  },
})

schema['fields']['body']['validate'] = (is_string,)
schema['fields']['replies_to_id']['validate'] = (is_required, is_uuid,)
