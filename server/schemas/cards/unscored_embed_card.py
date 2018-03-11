from modules.util import extend
from modules.validations import is_required, is_string, is_url
from schemas.card import schema as card_schema


schema = extend({}, card_schema, {
  'fields': {
    'data': {
      'url': {
        'validate': (is_required, is_string, is_url,)
      },
    },
  }
})
