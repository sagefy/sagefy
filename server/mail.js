const { createTransport } = require('nodemailer')
const { Client } = require('pg')
const jwt = require('jsonwebtoken')

const ROOT =
  process.env.NODE_ENV === 'production'
    ? 'https://sagefy.org'
    : 'http://localhost'

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
const WELCOME_SUBJECT = 'Welcome to Sagefy'
const WELCOME_TEXT = `
Welcome to Sagefy!

If you did not create this account, please reply immediately.

If you are interested in biweekly updates on Sagefy's progress,
sign up at https://sgfy.xyz/updates

Thank you!

${FOOTER_TEXT}
`
const PASSWORD_TOKEN_SUBJECT = 'Sagefy - Verification Request'
const PASSWORD_TOKEN_TEXT = `
To verify and update your account, please visit:
{ROOT}/password/edit?token={token}

If you did not request a password change, please reply immediately.

${FOOTER_TEXT}
`
const EMAIL_TOKEN_SUBJECT = 'Sagefy - Verification Request'
const EMAIL_TOKEN_TEXT = `
To verify and update your account, please visit:
{ROOT}/email/edit?token={token}

If you did not request an email change, please reply immediately.

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

const transport = createTransport(
  {
    host: 'smtp.mailgun.org',
    port: 587,
    // secure: true,
    auth: {
      user: SENDER,
      pass: process.env.MAIL_PASS,
    },
  },
  {
    from: SENDER,
  }
)

/* eslint-disable no-console */
async function sendMail({ to, subject, body }) {
  if (process.env.NODE_ENV === 'test') return Promise.resolve(subject)
  try {
    return await transport.sendMail({
      to,
      subject,
      text: body,
    })
  } catch (e) {
    console.log('Did not send mail.', e)
    return Promise.resolve()
  }
}
/* eslint-enable */

async function listenToNotification(msg) {
  if (msg.channel === 'create_user') {
    return sendMail({
      to: msg.payload,
      subject: WELCOME_SUBJECT,
      body: WELCOME_TEXT,
    })
  }
  if (msg.channel === 'send_password_token') {
    const [to, userId, uniq] = msg.payload.split(' ')
    const token = jwt.sign({ user_id: userId, uniq }, process.env.JWT_SECRET, {
      expiresIn: '1h',
      audience: 'postgraphile',
    })
    return sendMail({
      to,
      subject: PASSWORD_TOKEN_SUBJECT,
      body: PASSWORD_TOKEN_TEXT.replace('{token}', token).replace(
        '{ROOT}',
        ROOT
      ),
    })
  }
  if (msg.channel === 'send_email_token') {
    const [to, userId, uniq] = msg.payload.split(' ')
    const token = jwt.sign({ user_id: userId, uniq }, process.env.JWT_SECRET, {
      expiresIn: '1h',
      audience: 'postgraphile',
    })
    return sendMail({
      to,
      subject: EMAIL_TOKEN_SUBJECT,
      body: EMAIL_TOKEN_TEXT.replace('{token}', token).replace('{ROOT}', ROOT),
    })
  }
  if (msg.channel === 'update_email') {
    return sendMail({
      to: msg.payload,
      subject: EMAIL_SUBJECT,
      body: EMAIL_TEXT,
    })
  }
  if (msg.channel === 'update_password') {
    return sendMail({
      to: msg.payload,
      subject: PASSWORD_SUBJECT,
      body: PASSWORD_TEXT,
    })
  }
  return null
}

module.exports = async function mailer() {
  // Why not use a shared pool with postgraphile?
  // https://github.com/brianc/node-pg-pool/issues/40
  const client = new Client({
    user: process.env.DB_USER,
    host: process.env.NODE_ENV === 'test' ? 'localhost' : process.env.DB_HOST,
    database: process.env.DB_DATABASE,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
  })

  await client.connect()

  await client.query('LISTEN create_user')
  await client.query('LISTEN send_email_token')
  await client.query('LISTEN send_password_token')
  await client.query('LISTEN update_email')
  await client.query('LISTEN update_password')

  client.on('notification', listenToNotification)
}
