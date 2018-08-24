/*

const merge = require('lodash.merge')
const { div, h1, p, a, hr } = require('../../helpers/tags')
const userSchema = require('../../schemas/user')
const { createFieldsData, findGlobalErrors } = require('../../helpers/forms')
const form = require('../components/form.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const goLogin = require('../../helpers/go_login')

const fields = [
  {
    name: 'id',
    type: 'hidden',
  },
  {
    name: 'name',
    label: 'Name',
    placeholder: 'ex: Unicorn',
  },
  {
    name: 'email',
    label: 'Email',
    placeholder: 'ex: unicorn@example.com',
  },
  {
    name: 'settings.email_frequency',
    label: 'Email Frequency',
    options: [
      {
        label: 'Immediate',
      },
      {
        label: 'Daily',
      },
      {
        label: 'Weekly',
      },
      {
        label: 'Never',
      },
    ],
    inline: true,
  },
  {
    name: 'submit',
    type: 'submit',
    label: 'Update',
    icon: 'update',
  },
]

fields.forEach((field, index) => {
  fields[index] = merge({}, userSchema[field.name] || {}, field)
})

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }

  const user = data.users && data.users[data.currentUserID]
  if (!user) {
    return spinner()
  }

  const instanceFields = createFieldsData({
    schema: userSchema,
    fields,
    errors: data.errors,
    formData: merge(
      {},
      {
        id: user.id,
        name: user.name,
        email: user.email,
        'settings.email_frequency': user.settings.email_frequency,
      },
      data.formData
    ),
    sending: data.sending,
  })

  const globalErrors = findGlobalErrors({
    fields,
    errors: data.errors,
  })

  return div(
    { id: 'settings', className: 'page' },
    h1('Settings'),
    form({
      fields: instanceFields,
      errors: globalErrors,
    }),
    hr(),
    p(a({ href: '/password' }, icon('password'), ' Change my password.')),
    p(
      a(
        { href: 'https://gravatar.com' },
        icon('update'),
        ' Update my avatar on Gravatar.'
      )
    )
  )
}



const { getFormValues, parseFormValues } = require('../../helpers/forms')
const userSchema = require('../../schemas/user')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'submit #settings form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      let values = getFormValues(el)
      getTasks().updateFormData(values)
      const errors = getTasks().validateForm(values, userSchema, [
        'name',
        'email',
      ])
      if (errors && errors.length) {
        return
      }
      values = parseFormValues(values)
      getTasks().updateUser(values)
    },
  })
}

*/
