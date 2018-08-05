const Joi = require('joi')

const db = require('./index')

const topicSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().guid(),
  name: Joi.string(),
  entity_id: Joi.string().guid(),
  entity_kind: Joi.string().valid('card', 'unit', 'subject'),
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
