from modules.util import extend
from modules.validations import is_required, is_string
from schemas.card import schema as card_schema


schema = extend({}, card_schema, {
  'fields': {
    'data': {
      'body': {
        'validate': (is_required, is_string,)
      },
    },
  }
})
