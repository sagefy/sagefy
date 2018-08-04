const db = require('./index')

/*
CREATE TABLE notices (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id uuid NOT NULL REFERENCES users (id),
  kind notice_kind NOT NULL,
  data jsonb NOT NULL,
    # jsonb?: varies per kind
  read boolean NOT NULL DEFAULT FALSE,
  tags text[] NULL DEFAULT array[]::text[]
);

CREATE TYPE notice_kind as ENUM(
  'create_topic',
  'create_proposal',
  'block_proposal',
  'decline_proposal',
  'accept_proposal',
  'create_post',
  'come_back'
);


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

*/

async function getNotice(noticeId) {}

async function listNotices(userId, { limit = 10, offset = 0 }) {}

async function insertNotice(data) {}

async function updateNoticeAsRead(noticeId) {}

async function updateNoticeAsUnread(noticeId) {}

module.exports = {
  getNotice,
  listNotices,
  insertNotice,
  updateNoticeAsRead,
  updateNoticeAsUnread,
}
