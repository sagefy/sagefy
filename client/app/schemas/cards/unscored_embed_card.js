const { required } = require('../../helpers/validations')
const { extend } = require('../../helpers/utilities')
const cardSchema = require('../card')

module.exports = extend({}, cardSchema, {
  'data.url': {
    type: 'text',
    validations: [required],
  },
})
