from schemas.entity_base import schema as entity_schema
from modules.util import extend
from modules.validations import is_required, is_string, is_list, is_one_of


"""
A subject is a collection of units and other subjects.
Subjects can vary greatly in scale.
A graph is automatically formed based on the units and subjects specified.
"""

schema = extend({}, entity_schema, {
  'tablename': 'subjects',
  'fields': {
    'body': {
      'validate': (is_required, is_string,),
    },
    'members': {
      'validate': (is_required, is_list,),
      'embed_many': {
        'id': {
          'validate': (is_required, is_string,),
        },
        'kind': {
          'validate': (is_required, is_string, (
            is_one_of, 'unit', 'subject'
          )),
        }
      }
    }
  },
})
