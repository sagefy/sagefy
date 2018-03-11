from modules.util import extend
from modules.validations import is_required, is_string, is_one_of
from schemas.card import schema as card_schema


schema = extend({}, card_schema, {
  'fields': {
    'data': {
      'embed': {
        'site': {
          'validate': (is_required, is_string, (is_one_of, 'youtube', 'vimeo'),),
        },
        'video_id': {
          'validate': (is_required, is_string,),
        },
      },
    },
  },
})
