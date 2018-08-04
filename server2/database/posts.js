const db = require('./index')

/*
CREATE TABLE posts (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id uuid NOT NULL REFERENCES users (id),
  topic_id uuid NOT NULL REFERENCES topics (id),
  kind post_kind NOT NULL DEFAULT 'post',
  body text NULL CHECK (kind = 'vote' OR body IS NOT NULL),
  replies_to_id uuid NULL REFERENCES posts (id)
    CHECK (kind <> 'vote' OR replies_to_id IS NOT NULL),
  entity_versions jsonb NULL CHECK (kind <> 'proposal' or entity_versions IS NOT NULL),
    --- jsonb?: ISSUE cant ref, cant enum composite
  response boolean NULL CHECK (kind <> 'vote' OR response IS NOT NULL)
);

CREATE UNIQUE INDEX posts_vote_unique_idx ON posts (user_id, replies_to_id) WHERE kind = 'vote';

CREATE TYPE post_kind as ENUM(
  'post',
  'proposal',
  'vote'
);

schema = extend({}, default, {
  'tablename': 'posts',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'topic_id': {
      'validate': (is_required, is_uuid,),
    },
    'body': {
      'validate': (is_required, is_string,),
    },
    'kind': {
      'validate': (is_required, is_string,
                   (is_one_of, 'post', 'proposal', 'vote')),
      'default': 'post',
    },
    'replies_to_id': {
      'validate': (is_uuid,),
    },
  },
})

schema = extend({}, post_schema, {
  'fields': {
    'entity_versions': {
      'validate': (is_required, is_list, (has_min_length, 1)),
      'embed_many': {
        'id': {
          'validate': (is_required, is_string,),
        },
        'kind': {
          'validate': (is_required, is_string, (
            is_one_of, 'card', 'unit', 'subject',
          )),
        },
      },
    },
  },
})

schema = extend({}, post_schema, {
  'fields': {
    'response': {
      'validate': (is_required, is_boolean,),
    }
  },
})

schema['fields']['body']['validate'] = (is_string,)
schema['fields']['replies_to_id']['validate'] = (is_required, is_uuid,)


*/

async function getPost(postId) {}

async function listPostsByTopic(topicId) {}

async function listPostsByUser(userId) {}

async function listVotesByProposal(proposalId) {}

async function insertPost(data) {}

async function insertProposal(data) {}

async function insertVote(data) {}

async function updatePost(prev, data) {}

async function updateProposal(prev, data) {}

async function updateVote(prev, data) {}

module.exports = {
  getPost,
  listPostsByTopic,
  listPostsByUser,
  listVotesByProposal,
  insertPost,
  insertProposal,
  insertVote,
  updatePost,
  updateProposal,
  updateVote,
}
