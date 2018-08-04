const db = require('./index')

/*
users (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name text NOT NULL UNIQUE,
  email text NOT NULL UNIQUE CONSTRAINT email_check CHECK (email ~* '^\S+@\S+\.\S+$'),
  password varchar(60) NOT NULL CONSTRAINT pass_check CHECK (password ~* '^\$2a\$.*$'),
  settings jsonb NOT NULL --- jsonb?: add new settings without alter table
)


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

*/

async function getUser(params) {}

async function getUserById(userId) {}

async function getUserByEmail(email) {}

async function getUserByName(name) {}

async function listUsers() {}

async function listUsersByUserIds(userIds) {}

async function insertUser(data) {}

async function updateUser(prev, data) {}

async function updateUserPassword(prev, data) {}

async function deleteUser(userId) {}

module.exports = {
  getUser,
  getUserById,
  getUserByEmail,
  getUserByName,
  listUsers,
  listUsersByUserIds,
  insertUser,
  updateUser,
  updateUserPassword,
  deleteUser,
}
