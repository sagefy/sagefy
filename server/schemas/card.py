from schemas.entity_base import schema as entity_schema
from modules.util import extend
from modules.validations import is_required, is_uuid, is_list, is_string, \
    is_one_of, is_dict, is_list_of_uuids

"""
Cards are the smallest entity in the Sagefy data structure system.
A card represents a single learner activity.
A card could present information, ask the learner to answer a question,
collaborate with a small group to tackle a challenge,
or create other cards.
"""

scored_kinds = ('choice',)

peer_scored_kinds = tuple()

schema = extend({}, entity_schema, {
  'tablename': 'cards',
  'fields': {
    'unit_id': {
      'validate': (is_required, is_uuid,)
    },
    'require_ids': {
      'validate': (is_required, is_list, is_list_of_uuids),
      'default': [],
    },
    'kind': {
      'validate': (
        is_required,
        is_string,
        (
          is_one_of,
          'video',
          'page',
          'unscored_embed',
          'choice'
        )
      ),
    },
    'data': {
      'validate': (is_required, is_dict,),
      'default': {},
    },
  },
})
