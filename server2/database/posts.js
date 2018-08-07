const Joi = require('joi')
const db = require('./index')

const postSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().guid(),
  topic_id: Joi.string().guid(),
  kind: Joi.string().valid('post'),
  body: Joi.string(),
  replies_to_id: Joi.string().guid(),
})

const proposalSchema = postSchema.keys({
  kind: Joi.string().valid('proposal'),
  entity_versions: Joi.array()
    .items(
      Joi.object().keys({
        id: Joi.string().guid(),
        kind: Joi.string().valid('card', 'unit', 'subject'),
      })
    )
    .min(1),
})

const voteSchema = postSchema.keys({
  kind: Joi.string().valid('vote'),
  response: Joi.boolean(),
  body: Joi.string(),
  replies_to_id: Joi.string().guid(),
})

async function getPost(postId) {
  const query = `
    SELECT *
    FROM posts
    WHERE id = $id
    LIMIT 1;
  `
}

async function listPostsByTopic(topicId) {
  const query = `
    SELECT *
    FROM posts
    WHERE topic_id = $topic_id
    ORDER BY created ASC
    OFFSET $offset
    LIMIT $limit;
  `
}

async function listPostsByUser(userId) {
  const query = `
    SELECT *
    FROM posts
    WHERE user_id = $user_id
    ORDER BY created ASC;
  `
}

async function listVotesByProposal(proposalId) {
  const query = `
    SELECT *
    FROM posts
    WHERE kind = 'vote' AND replies_to_id = $proposal_id
    ORDER BY created DESC;
  `
}

async function insertPost(data) {
  const query = `
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,   replies_to_id  )
    VALUES
    ($user_id, $topic_id, $kind, $body, $replies_to_id)
    RETURNING *;
  `
}

async function insertProposal(data) {
  const query = `
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,
       replies_to_id  ,   entity_versions  )
    VALUES
    ($user_id, $topic_id, $kind, $body,
     $replies_to_id, $entity_versions)
    RETURNING *;
  `
}

async function insertVote(data) {
  const query = `
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,
       replies_to_id  ,   response  )
    VALUES
    ($user_id, $topic_id, $kind, $body,
     $replies_to_id, $response)
    RETURNING *;
  `
}

async function updatePost(prev, data) {
  const query = `
    UPDATE posts
    SET body = $body
    WHERE id = $id AND kind = 'post'
    RETURNING *;
  `
}

async function updateProposal(prev, data) {
  const query = `
    UPDATE posts
    SET body = $body
    WHERE id = $id AND kind = 'proposal'
    RETURNING *;
  `
}

async function updateVote(prev, data) {
  const query = `
    UPDATE posts
    SET body = $body, response = $response
    WHERE id = $id AND kind = 'vote'
    RETURNING *;
  `
}

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
