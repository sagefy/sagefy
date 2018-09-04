const Joi = require('joi')

// TODO additional checks

const db = require('./base')
const es = require('../helpers/es')

const topicSchema = Joi.object().keys({
  id: Joi.string().length(22),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().length(22),
  name: Joi.string(),
  entity_id: Joi.string().length(22),
  entity_kind: Joi.string().valid('card', 'unit', 'subject'),
})

async function sendTopicToEs(topic) {
  return es.index({
    index: 'entity',
    type: 'topic',
    body: topic,
    id: topic.id,
  })
}

async function getTopic(topicId) {
  const query = `
    SELECT *
    FROM topics
    WHERE id = $id
    LIMIT 1;
  `
  return db.get(query, { id: topicId })
}

async function listTopics() {
  const query = `
    SELECT *
    FROM topics
    ORDER BY created DESC;
  `
  return db.list(query)
}

async function listTopicsByEntityId(entityId) {
  const query = `
    SELECT *
    FROM topics
    WHERE entity_id = $entity_id
    ORDER BY created DESC;
  `
  return db.list(query, { entity_id: entityId })
}

async function insertTopic(params) {
  Joi.assert(params, topicSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO topics
    (  user_id  ,   entity_id  ,   entity_kind  ,   name  )
    VALUES
    ($user_id, $entity_id, $entity_kind, $name)
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendTopicToEs(data)
  return data
}

async function updateTopic(params) {
  Joi.assert(params, topicSchema.requiredKeys(Object.keys(params)))
  const query = `
    UPDATE topics
    SET name = $name
    WHERE id = $id
    RETURNING *;
  `
  const data = await db.save(query, params)
  await sendTopicToEs(data)
  return data
}

module.exports = {
  getTopic,
  listTopics,
  listTopicsByEntityId,
  insertTopic,
  updateTopic,
}
