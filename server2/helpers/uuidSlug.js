const slugid = require('slugid')
const Joi = require('joi')

const guidSchema = Joi.string().guid()
const slugSchema = Joi.string()
  .length(22)
  .regex(/^[0-9a-zA-Z\-_]+$/)
const isUuid = id => Joi.validate(id, guidSchema)
const isSlug = id => Joi.validate(id, slugSchema)

module.exports = {
  convertToUuid(id) {
    if (isSlug(id)) {
      return slugid.decode(id)
    }
    return id
  },

  convertToSlug(id) {
    if (isUuid(id)) {
      return slugid.encode(id)
    }
    return id
  },

  generateSlug() {
    return slugid.nice()
  },
}
