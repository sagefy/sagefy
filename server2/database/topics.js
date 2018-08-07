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

async function getTopic(topicId) {
  const query = `
    SELECT *
    FROM topics
    WHERE id = $id
    LIMIT 1;
  `
}

async function listTopics(params) {
  const query = `
    SELECT *
    FROM topics
    ORDER BY created DESC;
  `
}

async function listTopicsByEntityId(entityId) {
  const query = `
    SELECT *
    FROM topics
    WHERE entity_id = $entity_id
    ORDER BY created DESC;
  `
}

async function insertTopic(data) {
  const query = `
    INSERT INTO topics
    (  user_id  ,   entity_id  ,   entity_kind  ,   name  )
    VALUES
    ($user_id, $entity_id, $entity_kind, $name)
    RETURNING *;
  `
}

async function updateTopic(prev, data) {
  const query = `
    UPDATE topics
    SET name = $name
    WHERE id = $id
    RETURNING *;
  `
}

module.exports = {
  getTopic,
  listTopics,
  listTopicsByEntityId,
  insertTopic,
  updateTopic,
}
