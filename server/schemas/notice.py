from schemas.index import schema as default
from modules.util import extend
from modules.validations import is_required, is_uuid, is_string, is_one_of, \
    is_dict, is_boolean, is_list, is_list_of_strings


schema = extend({}, default, {
  'tablename': 'notices',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'kind': {
      'validate': (
        is_required,
        is_string,
        (
          is_one_of,
          'create_topic',
          'create_proposal',
          'block_proposal',
          'decline_proposal',
          'accept_proposal',
          'create_post',
          'come_back'
        ),
      ),
    },
    'data': {
      'validate': (is_required, is_dict,),
      'default': {},
    },
    'read': {
      'validate': (is_required, is_boolean),
      'default': False,
    },
    'tags': {
      'validate': (is_list, is_list_of_strings),
      'default': [],
    },
  }
})
