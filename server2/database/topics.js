const Joi = require('joi')

const db = require('./index')

const topicSchema = Joi.object().keys({
  id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  user_id: Joi.string()
    .guid()
    .required(),
  name: Joi.string().required(),
  entity_id: Joi.string()
    .guid()
    .required(),
  entity_kind: Joi.string()
    .valid('card', 'unit', 'subject')
    .required(),
})

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
