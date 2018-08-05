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

/*
insert_topic
  query = """
    INSERT INTO topics
    (  user_id  ,   entity_id  ,   entity_kind  ,   name  )
    VALUES
    (%(user_id)s, %(entity_id)s, %(entity_kind)s, %(name)s)
    RETURNING *;
  """

update_topic
  query = """
    UPDATE topics
    SET name = %(name)s
    WHERE id = %(id)s
    RETURNING *;
  """

get_topic
  query = """
    SELECT *
    FROM topics
    WHERE id = %(id)s
    LIMIT 1;
  """

list_topics
  query = """
    SELECT *
    FROM topics
    ORDER BY created DESC;
  """

list_topics_by_entity_id
  query = """
    SELECT *
    FROM topics
    WHERE entity_id = %(entity_id)s
    ORDER BY created DESC;
  """
*/

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
