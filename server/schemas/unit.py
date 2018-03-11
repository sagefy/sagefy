from schemas.entity_base import schema as entity_schema
from modules.util import extend
from modules.validations import is_required, is_string, is_list, \
  is_list_of_uuids

"""
A unit is the medium size in the Sagefy data structure system.
A unit represents a unit of learning activity.
A unit is defined by a single goal (objective). See Bloom's Taxonomy.
A unit should represent a goal that is as small as possible
without becoming systemically redundant.
An example of a unit is a small learning lesson,
which may contain about five to eight minutes of information and
30-60 minutes of practice to gain proficiency.
"""

schema = extend({}, entity_schema, {
  'tablename': 'units',
  'fields': {
    'body': {
      'validate': (is_required, is_string,),
    },
    'require_ids': {
      'validate': (is_required, is_list, is_list_of_uuids),
      'default': [],
    },
  },
})
