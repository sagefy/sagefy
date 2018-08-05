const Joi = require('joi')

const db = require('./index')

const followSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().guid(),
  entity_id: Joi.string().guid(),
  entity_kind: Joi.string().valid('card', 'unit', 'subject', 'topic'),
})

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
