from schemas.index import schema as default
from modules.util import extend
from modules.validations import is_required, is_uuid, is_string, is_one_of


schema = extend({}, default, {
  'tablename': 'posts',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'topic_id': {
      'validate': (is_required, is_uuid,),
    },
    'body': {
      'validate': (is_required, is_string,),
    },
    'kind': {
      'validate': (is_required, is_string,
                   (is_one_of, 'post', 'proposal', 'vote')),
      'default': 'post',
    },
    'replies_to_id': {
      'validate': (is_uuid,),
    },
  },
})
