const merge = require('lodash.merge')
const post = require('./post')
const { required } = require('../helpers/validations')

const noop = () => {}

module.exports = merge({}, post, {
  body: {
    type: 'textarea',
    validations: [noop],
  },
  replies_to_id: {
    type: 'hidden',
    validations: [required],
  },
  response: {
    type: 'select',
    validations: [required],
    options: [{ value: 'true' }, { value: 'false' }],
  },
})
