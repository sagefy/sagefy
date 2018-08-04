const db = require('./index')

/*
CREATE TABLE topics (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id uuid NOT NULL REFERENCES users (id),
  name text NOT NULL,
  entity_id uuid NOT NULL,  --- ISSUE cant ref across tables
  entity_kind entity_kind NOT NULL );

CREATE TYPE entity_kind AS ENUM(
  'card',
  'unit',
  'subject'
);



schema = extend({}, default, {
  'tablename': 'topics',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'name': {
      'validate': (is_required, is_string),
    },
    'entity_id': {
      'validate': (is_required, is_uuid,),
    },
    'entity_kind': {
      'validate': (is_required, is_string, (is_one_of, 'card', 'unit', 'subject')),
    },
  }
})

*/

async function getTopic(topicId) {}

async function listTopics(params) {}

async function listTopicsByEntityId(entityId) {}

async function insertTopic(data) {}

async function updateTopic(prev, data) {}

module.exports = {
  getTopic,
  listTopics,
  listTopicsByEntityId,
  insertTopic,
  updateTopic,
}
