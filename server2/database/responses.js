const Joi = require('joi')

const db = require('./index')

const responseSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  user_id: Joi.string().guid(),
  card_id: Joi.string().guid(),
  unit_id: Joi.string().guid(),
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
}

async function insertResponse(data) {
  const query = `
    INSERT INTO responses
    ( user_id,  card_id,  unit_id,
      response,  score,  learned)
    VALUES
    ($user_id, $card_id, $unit_id,
     $response, $score, $learned)
    RETURNING *;
  `
}

module.exports = {
  getLatestResponse,
  insertResponse,
}
