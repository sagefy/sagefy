const Joi = require('joi')

const db = require('./base')

// TODO add additional checks

const followSchema = Joi.object().keys({
  id: Joi.string().length(22),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().length(22),
  entity_id: Joi.string().length(22),
  entity_kind: Joi.string().valid('card', 'unit', 'subject', 'topic'),
})

async function getFollow(userId, entityId) {
  const query = `
    SELECT *
    FROM follows
    WHERE user_id = $user_id AND entity_id = $entity_id
    LIMIT 1;
  `
  return db.get(query, { user_id: userId, entity_id: entityId })
}

async function getFollowById(followId) {
  const query = `
    SELECT *
    FROM follows
    WHERE id = $id
    LIMIT 1;
  `
  return db.get(query, { id: followId })
}

async function listFollowsByUser(userId) {
  const query = `
    SELECT *
    FROM follows
    WHERE user_id = $user_id
    ORDER BY created DESC;
  `
  return db.list(query, { user_id: userId })
}

async function listFollowsByEntity({ entityId, entityKind }) {
  const query = `
    SELECT *
    FROM follows
    WHERE entity_id = $entity_id AND entity_kind = $entity_kind
    ORDER BY created DESC;
  `
  return db.list(query, { entity_id: entityId, entity_kind: entityKind })
}

async function insertFollow(params) {
  Joi.assert(params, followSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO follows
    ( user_id,  entity_id,  entity_kind)
    VALUES
    ($user_id, $entity_id, $entity_kind)
    RETURNING *;
  `
  const data = await db.save(query, params)
  return data
}

async function deleteFollow(followId) {
  const query = `
    DELETE FROM follows
    WHERE id = $id;
  `
  return db.save(query, { id: followId })
}

module.eports = {
  getFollow,
  getFollowById,
  listFollowsByUser,
  listFollowsByEntity,
  insertFollow,
  deleteFollow,
}
