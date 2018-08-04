const Joi = require('joi')

const db = require('./index')

const followSchema = Joi.object().keys({
  id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  user_id: Joi.string()
    .guid()
    .required(),
  entity_id: Joi.string()
    .guid()
    .required(),
  entity_kind: Joi.string()
    .valid('card', 'unit', 'subject', 'topic')
    .required(),
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
