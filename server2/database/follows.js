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

async function getFollow(userId, entityId) {
  const query = `
    SELECT *
    FROM follows
    WHERE user_id = $user_id AND entity_id = $entity_id
    LIMIT 1;
  `
}

async function getFollowById(followId) {
  const query = `
    SELECT *
    FROM follows
    WHERE id = $id
    LIMIT 1;
  `
}

async function listFollowsByUser(userId) {
  const query = `
    SELECT *
    FROM follows
    WHERE user_id = $user_id
    ORDER BY created DESC;
  `
}

async function listFollowsByEntity({ entityId, entityKind }) {
  const query = `
    SELECT *
    FROM follows
    WHERE entity_id = $entity_id AND entity_kind = $entity_kind
    ORDER BY created DESC;
  `
}

async function insertFollow(data) {
  const query = `
    INSERT INTO follows
    ( user_id,  entity_id,  entity_kind)
    VALUES
    ($user_id, $entity_id, $entity_kind)
    RETURNING *;
  `
}

async function deleteFollow(followId) {
  const query = `
    DELETE FROM follows
    WHERE id = $id;
  `
}

module.eports = {
  getFollow,
  getFollowById,
  listFollowsByUser,
  listFollowsByEntity,
  insertFollow,
  deleteFollow,
}
