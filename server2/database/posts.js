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
