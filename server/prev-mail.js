/*

const mailer = require('./mail')

mailer(client)

*/

const { createTransport } = require('nodemailer')

const SENDER = 'support@sagefy.org'

const transport = createTransport(
  {
    // process.env.MAIL...
  },
  {
    from: SENDER,
  }
)

export async function sendMail({ to, subject, body }) {
  if (process.env.NODE_ENV === 'test') return Promise.resolve()
  return transport.sendMail({
    to,
    subject,
    text: body,
  })
}

const FOOTER_TEXT = `
This is a transactional email from Sagefy.
We are required to notify you of sign ups, password changes,
and any security incidents while you have an account.
If you would like to unsubscribe from other types of notices
or if you would like to delete your account,
please reply to this email and let us know.
We will fulfill your request within 10 business days.
`
const WELCOME_SUBJECT = 'Welcome to Sagefy'
const WELCOME_TEXT = `
Welcome to Sagefy!

If you did not create this account, please reply immediately.

If you are interested in biweekly updates on Sagefy's progress,
sign up at https://sgef.cc/devupdates

Thank you!

${FOOTER_TEXT}
`
const TOKEN_SUBJECT = 'Sagefy - Verification Request'
const TOKEN_TEXT = `
To verify and update your account, please visit:
https://sagefy.org/private?token={token}

If you did not request an email or password change, please reply immediately.

${FOOTER_TEXT}
`
const EMAIL_SUBJECT = 'Sagefy - Email Updated'
const EMAIL_TEXT = `
You updated your Sagefy email.

If you did not change your email, please reply immediately.

${FOOTER_TEXT}
`
const PASSWORD_SUBJECT = 'Sagefy - Password Updated'
const PASSWORD_TEXT = `
You updated your Sagefy password.

If you did not change your password, please reply immediately.

${FOOTER_TEXT}
`

export default function mailer(client) {
  client.on('notification', async msg => {
    if (msg.channel === 'create_user') {
      await sendMail({
        to: msg.payload,
        subject: WELCOME_SUBJECT,
        body: WELCOME_TEXT,
      })
    }
    if (msg.channel === 'send_reset_token') {
      const [to, token] = msg.payload.split(' ')
      await sendMail({
        to,
        subject: TOKEN_SUBJECT,
        body: TOKEN_TEXT.replace('{token}', token),
      })
    }
    if (msg.channel === 'update_email') {
      await sendMail({
        to: msg.payload,
        subject: EMAIL_SUBJECT,
        body: EMAIL_TEXT,
      })
    }
    if (msg.channel === 'update_password') {
      await sendMail({
        to: msg.payload,
        subject: PASSWORD_SUBJECT,
        body: PASSWORD_TEXT,
      })
    }
  })
}
