from schemas.index import schema as default
from modules.validations import is_required, is_string, has_min_length, \
  is_one_of, is_email, is_dict
from modules.util import extend
from passlib.hash import bcrypt


def encrypt_password(value):
  if value and not value.startswith('$2a$'):
    return bcrypt.encrypt(value)
  return value


schema = extend({}, default, {
  'tablename': 'users',
  'fields': {
    'modified': {
      'access': ('private',),
    },
    'name': {
      'validate': (is_required, is_string, (has_min_length, 1),),
    },
    'email': {
      'validate': (is_required, is_string, (has_min_length, 1), is_email,),
      'access': ('private',),
    },
    'password': {
      'validate': (is_required, is_string, (has_min_length, 8),),
      'access': ('PaSsWoRd',),
      'bundle': encrypt_password,
    },
    'settings': {
      'validate': (is_required, is_dict),
      'default': {},
      'embed': {
        'email_frequency': {
          'validate': (is_required, is_string, (
            is_one_of, 'immediate', 'daily', 'weekly', 'never',
          )),
          'access': ('private',),
          'default': 'daily',
        },
        'view_subjects': {
          'validate': (is_required, is_string, (
            is_one_of, 'public', 'private'
          )),
          'default': 'private',
        },
        'view_follows': {
          'validate': (is_required, is_string, (
            is_one_of, 'public', 'private'
          )),
          'default': 'private',
        },
      }
    }
  },
})
