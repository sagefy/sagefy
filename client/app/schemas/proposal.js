const post = require('./post')
const { extend } = require('../helpers/utilities')
const { required } = require('../helpers/validations')

module.exports = extend({}, post, {
  'entity_version.id': {
    type: 'hidden',
    validations: [],
  },
  'entity_version.kind': {
    type: 'select',
    options: [{ value: 'card' }, { value: 'unit' }, { value: 'subject' }],
    validations: [required],
  },
})
