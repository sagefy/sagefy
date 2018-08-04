const Joi = require('joi')

const db = require('./index')

const responseSchema = Joi.object().keys({
  id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  user_id: Joi.string()
    .guid()
    .required(),
  card_id: Joi.string()
    .guid()
    .required(),
  unit_id: Joi.string()
    .guid()
    .required(),
  response: Joi.string().required(),
  score: Joi.number()
    .min(0)
    .max(1)
    .required(),
  learned: Joi.number()
    .min(0)
    .max(1)
    .required(),
})

async function getLatestResponse(userId, unitId) {}

async function insertResponse(data) {}

module.exports = {
  getLatestResponse,
  insertResponse,
}
