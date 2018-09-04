const Joi = require('joi')
const db = require('./base')
const es = require('../helpers/es')

// TODO add additional checks

const postSchema = Joi.object().keys({
  id: Joi.string().length(22),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().length(22),
  topic_id: Joi.string().length(22),
  kind: Joi.string().valid('post'),
  body: Joi.string(),
  replies_to_id: Joi.string().length(22),
})

const proposalSchema = postSchema.keys({
  kind: Joi.string().valid('proposal'),
  entity_versions: Joi.array()
    .items(
      Joi.object().keys({
        id: Joi.string().length(22),
        kind: Joi.string().valid('card', 'unit', 'subject'),
      })
    )
    .min(1),
})

const voteSchema = postSchema.keys({
  kind: Joi.string().valid('vote'),
  response: Joi.boolean(),
  body: Joi.string(),
  replies_to_id: Joi.string().length(22),
})

async function sendPostToEs(post) {
  return es.index({
    index: 'entity',
    type: 'post',
    body: post,
    id: post.id,
  })
}

async function getPost(postId) {
  const query = `
    SELECT *
    FROM posts
    WHERE id = $id
    LIMIT 1;
  `
  return db.get(query, { id: postId })
}

async function listPostsByTopic(topicId, { limit = 10, offset = 0 }) {
  const query = `
    SELECT *
    FROM posts
    WHERE topic_id = $topic_id
    ORDER BY created ASC
    OFFSET $offset
    LIMIT $limit;
  `
  return db.list(query, { topic_id: topicId, limit, offset })
}

async function listPostsByUser(userId) {
  const query = `
    SELECT *
    FROM posts
    WHERE user_id = $user_id
    ORDER BY created ASC;
  `
  return db.list(query, { user_id: userId })
}

async function listVotesByProposal(proposalId) {
  const query = `
    SELECT *
    FROM posts
    WHERE kind = 'vote' AND replies_to_id = $proposal_id
    ORDER BY created DESC;
  `
  return db.list(query, { proposal_id: proposalId })
}

async function insertPost(params) {
  Joi.assert(params, postSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,   replies_to_id  )
    VALUES
    ($user_id, $topic_id, $kind, $body, $replies_to_id)
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendPostToEs(data)
  return data
}

async function insertProposal(params) {
  Joi.assert(params, proposalSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,
       replies_to_id  ,   entity_versions  )
    VALUES
    ($user_id, $topic_id, $kind, $body,
     $replies_to_id, $entity_versions)
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendPostToEs(data)
  return data
}

async function insertVote(params) {
  Joi.assert(params, voteSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO posts
    (  user_id  ,   topic_id  ,   kind  ,   body  ,
       replies_to_id  ,   response  )
    VALUES
    ($user_id, $topic_id, $kind, $body,
     $replies_to_id, $response)
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendPostToEs(data)
  return data
}

async function updatePost(params) {
  Joi.assert(params, postSchema.requiredKeys(Object.keys(params)))
  const query = `
    UPDATE posts
    SET body = $body
    WHERE id = $id AND kind = 'post'
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendPostToEs(data)
  return data
}

async function updateProposal(params) {
  Joi.assert(params, proposalSchema.requiredKeys(Object.keys(params)))
  const query = `
    UPDATE posts
    SET body = $body
    WHERE id = $id AND kind = 'proposal'
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendPostToEs(data)
  return data
}

async function updateVote(params) {
  Joi.assert(params, voteSchema.requiredKeys(Object.keys(params)))
  const query = `
    UPDATE posts
    SET body = $body, response = $response
    WHERE id = $id AND kind = 'vote'
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendPostToEs(data)
  return data
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
