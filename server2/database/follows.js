const db = require('./index')

/*
CREATE TYPE follow_kind AS ENUM(
  'card',
  'unit',
  'subject',
  'topic'
);

CREATE TABLE follows (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id uuid NOT NULL REFERENCES users (id),
  entity_id uuid NOT NULL, --- ISSUE cant ref across tables
  entity_kind follow_kind NOT NULL,
  UNIQUE (user_id, entity_id)
);


schema = extend({}, default, {
  'tablename': 'follows',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'entity_id': {
      'validate': (is_required, is_uuid,),
    },
    'entity_kind': {
      'validate': (
        is_required,
        is_string,
        (
          is_one_of,
          'card',
          'unit',
          'subject',
          'topic'
        ),
      ),
    },
  },
})

*/

async function getFollow(userId, entityId) {}

async function getFollowById(followId) {}

async function listFollowsByUser(userId) {}

async function listFollowsByEntity({ entityId, entityKind }) {}

async function insertFollow(data) {}

async function deleteFollow(followId) {}

module.eports = {
  getFollow,
  getFollowById,
  listFollowsByUser,
  listFollowsByEntity,
  insertFollow,
  deleteFollow,
}
