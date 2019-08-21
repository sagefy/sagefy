const get = require('lodash.get')
const toPairs = require('lodash.topairs')

const FIELD_REGEXP = /^<(.*?)>/i

const KNOWN_ERRORS = toPairs({
  email_check: '<email> Please format your email like `a@b.c`.',
  pass_check: '<password> I saw an unfamiliar error.',
  user_email_key: "<email> I've seen this email address before.",
  user_pkey: ' I saw an unfamiliar error.',
  user_name_key: "<name> I've seen this name before.",
  create_user: ' I am unable to send you an email to create your account.',
  user_user_id_fkey: ' I saw an unfamiliar error.',
  '355CAC69': '<password> I need at least 8 characters for passwords.',
  '51EA51A9': "<password> Your password didn't match.",
  '3883C744': "<email> I didn't find an account with that email.",
  '4F811CFE': "<name> I couldn't find a matching account.",
  '58483A61': " I couldn't update your email.",
  EBC6E992: " I couldn't update your password.",
  EE05C989: 'No card found.',
  '1306BF1C': 'You may only respond to a scored card.',
  '681942FD': 'You must submit an available response `id`.',
  '5E310F2E': '<name> Subject name in use.',
  '76177573': 'A reply must belong to the same topic.',
  '8DF72C56': 'A vote may only reply to a proposal.',
  E47E0411: 'A user cannot vote on their own proposal.',
  '47C88D24': 'No user found.',
  CF018471: 'No previous version found.',
  B7615F09: 'No previous version found.',
}).map(([key, message]) => ({
  key,
  field: get(message.match(FIELD_REGEXP), 1, undefined),
  message: message.replace(FIELD_REGEXP, ''),
}))

const DEFAULT_FIELD = 'all'

module.exports = function getGqlErrors(e) {
  if (process.env.NODE_ENV !== 'production') console.error(e) // eslint-disable-line
  return get(e, 'response.errors', [])
    .map(({ message }) =>
      get(KNOWN_ERRORS.filter(({ key }) => message.indexOf(key) > -1), 0, {
        message,
      })
    )
    .reduce((sum, { message, field }) => {
      const xfield = field || DEFAULT_FIELD
      sum[xfield] = sum[xfield] || [] // eslint-disable-line
      sum[xfield].push(message) // eslint-disable-line
      return sum
    }, {})
}
