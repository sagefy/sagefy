const merge = require('lodash.merge')
const post = require('./post')
const { required } = require('../helpers/validations')

module.exports = merge({}, post, {
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
