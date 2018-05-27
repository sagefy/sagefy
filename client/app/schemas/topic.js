const { required } = require('../helpers/validations')

module.exports = {
  id: {
    type: 'hidden',
    validations: [],
  },
  name: {
    type: 'text',
    validations: [required],
  },
  entity_id: {
    type: 'hidden',
    validations: [required],
  },
  entity_kind: {
    type: 'hidden',
    validations: [required],
  },
}
