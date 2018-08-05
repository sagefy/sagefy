const { createTransport } = require('nodemailer')

const config = require('../config')

const SENDER = 'support@sagefy.org'
const FOOTER_TEXT = `

This is a transactional email from Sagefy.
We are required to notify you of sign ups, password changes,
and any security incidents while you have an account.
If you would like to unsubscribe from other types of notices
or if you would like to delete your account,
please reply to this email and let us know.
We will fulfill your request within 10 business days.
`

const transport = createTransport(config.mail, {
  from: SENDER,
})

module.exports = async function sendMail({ to, subject, body }) {
  if (config.test) return Promise.resolve()
  return transport.sendMail({
    to,
    subject,
    text: body + FOOTER_TEXT,
  })
}
