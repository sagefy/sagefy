const post = require('./post')
const { extend } = require('../helpers/utilities')
const { required } = require('../helpers/validations')

const noop = () => {}

module.exports = extend({}, post, {
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
