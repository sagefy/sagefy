const get = require('lodash.get')

const KNOWN_ERRORS = [
  {
    key: 'email_check',
    field: 'email',
    message: 'Please format your email like `a@b.c`.',
  },
  {
    key: 'pass_check',
    field: 'password',
    message: 'I saw an unfamiliar error.',
  },
  {
    key: 'user_email_key',
    field: 'email',
    message: "I've seen this email address before.",
  },
  { key: 'user_pkey', message: 'I saw an unfamiliar error.' },
  {
    key: 'user_name_key',
    field: 'name',
    message: "I've seen this name before.",
  },
  {
    key: 'create_user',
    message: 'I am unable to send you an email to create your account.',
  },
  { key: 'user_user_id_fkey', message: 'I saw an unfamiliar error.' },
  {
    key: '355CAC69',
    field: 'password',
    message: 'I need at least 8 characters for passwords.',
  },
  {
    key: '51EA51A9',
    field: 'password',
    message: "Your password didn't match.",
  },
  {
    key: '3883C744',
    field: 'email',
    message: "I didn't find an account with that email.",
  },
  {
    key: '4F811CFE',
    field: 'name',
    message: "I couldn't find a matching account.",
  },
  {
    key: '58483A61',
    message: "I couldn't update your email.",
  },
  {
    key: 'EBC6E992',
    message: "I couldn't update your password.",
  },
]

const DEFAULT_FIELD = 'all'

module.exports = function getGqlErrors(e) {
  return get(e, 'response.errors', [])
    .map(({ message }) => {
      const found = KNOWN_ERRORS.find(({ key }) => message.indexOf(key) > -1)
      return {
        message: get(found, 'message', message),
        field: get(found, 'field', undefined),
      }
    })
    .reduce((sum, { message, field }) => {
      const xfield = field || DEFAULT_FIELD
      sum[xfield] = sum[xfield] || [] // eslint-disable-line
      sum[xfield].push(message) // eslint-disable-line
      return sum
    }, {})
}
