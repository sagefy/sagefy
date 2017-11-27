const post = require('./post')
const { extend } = require('../modules/utilities')
const { required } = require('../modules/validations')

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
