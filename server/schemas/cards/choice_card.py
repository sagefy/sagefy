from modules.content import get as c
from modules.util import extend, create_uuid_b64
from modules.validations import is_required, is_string, is_list, \
  is_one_of, is_boolean, is_integer, has_min_length
from schemas.card import schema as card_schema


def has_correct_options(options):
  """
  Ensure the list of options has at least one correct option.
  """

  has_correct = False
  for option in options:
    if option.get('correct') is True:
      has_correct = True
  if not has_correct:
    return c('error_need_correct')


schema = extend({}, card_schema, {
  'fields': {
    'data': {
      'embed': {
        'body': {  # Question field
          'validate': (is_required, is_string,),
        },
        'options': {  # Available answers
          'validate': (is_required, is_list, (has_min_length, 1), has_correct_options),
          'embed_many': {
            'id': {
              'validate': (is_required, is_string,),
              'default': create_uuid_b64,
            },
            'value': {
              'validate': (is_required, is_string,),
            },
            'correct': {
              'validate': (is_required, is_boolean,),
              'access': ('view',),
            },
            'feedback': {
              'validate': (is_required, is_string,),
              'access': ('view',),
            },
          }
        },
        'order': {
          'validate': (is_string, (is_one_of, 'random', 'set')),
          'default': 'random',
          'access': ('view',),
        },
        'max_options_to_show': {
          'validate': (is_integer,),
          'default': 4,
          'access': ('view',),
        },
      },
    },
  },
})
