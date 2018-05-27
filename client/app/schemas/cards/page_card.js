const { required } = require('../../helpers/validations')
const { extend } = require('../../helpers/utilities')
const cardSchema = require('../card')

module.exports = extend({}, cardSchema, {
  'data.body': {
    type: 'textarea',
    validations: [required],
  },
})
