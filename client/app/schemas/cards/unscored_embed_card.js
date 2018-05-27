const merge = require('lodash.merge')
const { required } = require('../../helpers/validations')
const cardSchema = require('../card')

module.exports = merge({}, cardSchema, {
  'data.url': {
    type: 'text',
    validations: [required],
  },
})
