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

async function getLatestResponse(userId, unitId) {}

async function insertResponse(data) {}

module.exports = {
  getLatestResponse,
  insertResponse,
}
