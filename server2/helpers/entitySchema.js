const Joi = require('joi')

module.exports = Joi.object().keys({
  version_id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  entity_id: Joi.string()
    .guid()
    .required(),
  previous_id: Joi.string().guid(),
  language: Joi.string()
    .regex(/^\w{2}(-\w{2})?$/)
    .required(),
  name: Joi.string().required(),
  status: Joi.string()
    .valid('pending', 'blocked', 'declined', 'accepted')
    .required(),
  available: Joi.boolean().required(),
  tags: Joi.array()
    .items(Joi.string().min(1))
    .required(),
  user_id: Joi.string()
    .guid()
    .required(),
})
