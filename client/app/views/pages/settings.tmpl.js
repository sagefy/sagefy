const { div, h1, p, a, hr } = require('../../helpers/tags')
const userSchema = require('../../schemas/user')
const { extend } = require('../../helpers/utilities')
const {
  createFieldsData,
  findGlobalErrors,
} = require('../../helpers/auxiliaries')
const form = require('../components/form.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const { goLogin } = require('../../helpers/auxiliaries')

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
  fields[index] = extend({}, userSchema[field.name] || {}, field)
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
    formData: extend(
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
