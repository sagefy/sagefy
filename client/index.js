/* eslint-disable max-params, no-console */
const path = require('path')
const express = require('express')
const bodyParser = require('body-parser')
const get = require('lodash.get')
const request = require('./request')

require('express-async-errors')

const cacheHash =
  process.env.NODE_ENV === 'test' ? '_' : Date.now().toString(36)

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
]

const app = express()

app.use(bodyParser.urlencoded({ extended: false }))

// See https://github.com/reactjs/express-react-views#add-it-to-your-app
app.set('views', path.join(__dirname, '/views'))
app.set('view engine', 'jsx')
app.engine('jsx', require('express-react-views').createEngine())

app.get('/sitemap.txt', (req, res) =>
  res.send(`
https://sagefy.org
https://sagefy.org/terms
https://sagefy.org/contact
https://sagefy.org/sign-up
`)
) // TODO

// Form submission handlers
app.post('/sign-up', async (req, res) => {
  const query = `mutation ($name: String!, $email: String!, $password: String!) {
  signUp(input: {name: $name, email: $email, password: $password}) {
    user {
      id
    }
  }
}`
  const xRes = await request(
    JSON.stringify({
      query,
      variables: req.body,
    })
  )
  if (get(xRes, 'errors')) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      formErrors: get(xRes, 'errors')
        .map(({ message }) => {
          const found = KNOWN_ERRORS.find(
            ({ key }) => message.indexOf(key) > -1
          )
          return {
            message: get(found, 'message', message),
            field: get(found, 'field', undefined),
          }
        })
        .reduce((sum, { message, field }) => {
          sum[field || 'all'] = sum[field || 'all'] || [] // eslint-disable-line
          sum[field || 'all'].push(message)
          return sum
        }, {}),
      prevValues: req.body,
    })
  }
  return res.redirect('/dashboard')
})

// For pages that don't have specific data requirements
app.get('*', (req, res) =>
  res.render('Index', { location: req.url, cacheHash })
)

// See express-async-errors
app.use((err, req, res, next) => {
  if (err && err.message) {
    res.status(403)
    res.json({ error: err.message })
  }
  next(err)
})

app.listen(process.env.PORT || 5984)

module.exports = app
