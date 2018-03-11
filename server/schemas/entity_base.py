from schemas.index import schema as default
from modules.util import extend
from modules.validations import is_required, is_uuid, is_string, is_language, \
    is_one_of, is_boolean, is_list, is_list_of_strings

"""
The model represents a **version** of an entity, not an entity itself.
The `entity_id` attribute is what refers to a particular entity.
The `id` attribute refers to a specific version of the entity.
The `previous_id` attribute refers to the version based off.
"""

schema = extend({}, default, {
  'fields': {
    'version_id': {
      'validate': (is_uuid,),
    },
    'entity_id': {
      'validate': (is_required, is_uuid,),
    },
    'previous_id': {
      'validate': (is_uuid,),
    },
    'language': {
      'validate': (is_required, is_string, is_language,),
      'default': 'en',
    },
    'name': {
      'validate': (is_required, is_string,),
    },
    'status': {
      'validate': (
        is_required,
        is_string,
        (
          is_one_of,
          'pending',
          'blocked',
          'declined',
          'accepted'
        ),
      ),
      'default': 'pending',
    },
    'available': {
      'validate': (is_required, is_boolean,),
      'default': True,
    },
    'tags': {
      'validate': (is_list, is_list_of_strings,),
      'default': [],
    },
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
  },
})

del schema['fields']['id']
