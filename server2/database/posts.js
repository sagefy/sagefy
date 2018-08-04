const Joi = require('joi')
const db = require('./index')

const postSchema = Joi.object().keys({
  id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  user_id: Joi.string()
    .guid()
    .required(),
  topic_id: Joi.string()
    .guid()
    .required(),
  kind: Joi.string()
    .valid('post')
    .required(),
  body: Joi.string().required(),
  replies_to_id: Joi.string().guid(),
})

const proposalSchema = postSchema.keys({
  kind: Joi.string()
    .valid('proposal')
    .required(),
  entity_versions: Joi.array()
    .items(
      Joi.object().keys({
        id: Joi.string()
          .guid()
          .required(),
        kind: Joi.string()
          .valid('card', 'unit', 'subject')
          .required(),
      })
    )
    .min(1)
    .required(),
})

const voteSchema = postSchema.keys({
  kind: Joi.string()
    .valid('vote')
    .required(),
  response: Joi.boolean().required(),
  body: Joi.string(),
  replies_to_id: Joi.string()
    .guid()
    .required(),
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
