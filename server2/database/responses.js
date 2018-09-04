const Joi = require('joi')

const db = require('./base')

const responseSchema = Joi.object().keys({
  id: Joi.string().length(22),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().length(22),
  card_id: Joi.string().length(22),
  unit_id: Joi.string().length(22),
  response: Joi.string(),
  score: Joi.number()
    .min(0)
    .max(1),
  learned: Joi.number()
    .min(0)
    .max(1),
})

async function getLatestResponse(userId, unitId) {
  const query = `
    SELECT *
    FROM responses
    WHERE user_id = $user_id AND unit_id = $unit_id
    ORDER BY created DESC
    LIMIT 1;
  `
  return db.get(query, { user_id: userId, unit_id: unitId })
}

async function insertResponse(params) {
  Joi.assert(params, responseSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO responses
    ( user_id,  card_id,  unit_id,
      response,  score,  learned)
    VALUES
    ($user_id, $card_id, $unit_id,
     $response, $score, $learned)
    RETURNING *;
  `
  const data = await db.save(query, params)
  return data
}

module.exports = {
  getLatestResponse,
  insertResponse,
}
