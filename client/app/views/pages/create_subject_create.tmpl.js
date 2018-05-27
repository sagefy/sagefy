const merge = require('lodash.merge')
const { div, h1 } = require('../../helpers/tags')
const subjectSchema = require('../../schemas/subject')
const form = require('../components/form.tmpl')
const {
  createFieldsData,
  findGlobalErrors,
} = require('../../helpers/auxiliaries')
const { getIsLoggedIn } = require('../../selectors/base')
const spinner = require('../components/spinner.tmpl')
const { goLogin } = require('../../helpers/auxiliaries')

const fields = [
  {
    label: 'Subject Name',
    name: 'name',
  },
  {
    label: 'Subject Language',
    name: 'language',
    options: [{ label: 'English' }],
    value: 'en',
  },
  {
    label: 'Subject Goal',
    description:
      'Start with a verb, such as: Compute the value of dividing two whole numbers.',
    name: 'body',
  },
  {
    name: 'members',
    label: 'Subject Members',
    description: 'Choose a list of units and subjects. Cycles are not allowed.',
    add: {
      label: 'Add an Existing Unit or Subject',
      url: '#',
    },
  },
  {
    type: 'submit',
    name: 'submit',
    label: 'Create Subject',
    icon: 'create',
  },
]

fields.forEach((field, index) => {
  fields[index] = merge({}, subjectSchema[field.name] || {}, field)
})

module.exports = function createSubjectCreate(data) {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }

  const instanceFields = createFieldsData({
    schema: subjectSchema,
    fields,
    errors: data.errors,
    formData: data.create.subject || {},
    sending: data.sending,
  })

  const globalErrors = findGlobalErrors({
    fields,
    errors: data.errors,
  })

  return div(
    { id: 'create', className: 'page create--subject-create' },
    h1('Create a New Subject'),
    form({
      fields: instanceFields,
      errors: globalErrors,
    })
  )
}
