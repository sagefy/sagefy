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

/*
get_follow
  query = """
    SELECT *
    FROM follows
    WHERE user_id = %(user_id)s AND entity_id = %(entity_id)s
    LIMIT 1;
  """

get_follow_by_id
  query = """
    SELECT *
    FROM follows
    WHERE id = %(id)s
    LIMIT 1;
  """

list_follows_by_user
  query = """
    SELECT *
    FROM follows
    WHERE user_id = %(user_id)s
    ORDER BY created DESC;
  """

list_follows_by_entity
  query = """
    SELECT *
    FROM follows
    WHERE entity_id = %(entity_id)s AND entity_kind = %(entity_kind)s
    ORDER BY created DESC;
  """

insert_follow
  query = """
    INSERT INTO follows
    (  user_id  ,   entity_id  ,   entity_kind  )
    VALUES
    (%(user_id)s, %(entity_id)s, %(entity_kind)s)
    RETURNING *;
  """

delete_follow
  query = """
    DELETE FROM follows
    WHERE id = %(id)s;
  """
*/

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
