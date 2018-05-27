const merge = require('lodash.merge')
const { div, h1, p, br, a } = require('../../helpers/tags')
const form = require('../components/form.tmpl')
const icon = require('../components/icon.tmpl')
const userSchema = require('../../schemas/user')
const {
  createFieldsData,
  findGlobalErrors,
} = require('../../helpers/auxiliaries')
const { getIsLoggedIn } = require('../../selectors/base')
const spinner = require('../components/spinner.tmpl')

const fields = [
  {
    name: 'name',
    label: 'Name or Email',
    placeholder: 'e.g. Unicorn',
  },
  {
    name: 'password',
    label: 'Password',
    placeholder: '',
  },
  {
    type: 'submit',
    name: 'log-in',
    label: 'Log In',
    icon: 'log-in',
  },
]

fields.forEach((field, index) => {
  fields[index] = merge({}, userSchema[field.name] || {}, field)
})

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (data.currentUserID) {
    div('Logged in already.')
  }

  const instanceFields = createFieldsData({
    schema: userSchema,
    fields,
    errors: data.errors,
    formData: data.formData,
    sending: data.sending,
  })

  const globalErrors = findGlobalErrors({
    fields,
    errors: data.errors,
  })

  return div(
    { id: 'log-in', className: 'page' },
    h1('Log In'),
    p(
      "Don't have an account? ",
      a({ href: '/sign_up' }, icon('sign-up'), ' Sign Up'),
      '.',
      br(),
      'Forgot your password? ',
      a({ href: '/password' }, icon('password'), ' Reset'),
      '.'
    ),
    form({
      fields: instanceFields,
      errors: globalErrors,
    })
  )
}
