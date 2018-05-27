const { required } = require('../helpers/validations')

module.exports = {
  language: {
    type: 'select',
    validations: [required],
    options: [{ value: 'en' }],
  },
  name: {
    type: 'text',
    validations: [required],
  },
  body: {
    type: 'textarea',
    validations: [required],
  },
  tags: {
    type: 'list',
    validations: [],
    columns: [{ name: 'tag', type: 'text' }],
  },
  members: {
    type: 'entities',
    validations: [],
    /*
      kind: (unit|subject)
      id
    */
  },
}
