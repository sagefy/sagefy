/* eslint-disable max-params, no-console */
const path = require('path')
const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const fs = require('fs')
const jwt = require('jsonwebtoken')
const gqlRequest = require('./gql-request')
const getFormErrors = require('./selectors/form-errors')

const gql = {
  rootNewUser: fs.readFileSync('./graphql/root-new-user.graphql', 'utf8'),
}

const cacheHash =
  process.env.NODE_ENV === 'test' ? '_' : Date.now().toString(36)

require('express-async-errors')

const app = express()

app.use(bodyParser.urlencoded({ extended: false }))
app.use(cookieParser())

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
https://sagefy.org/log-in
https://sagefy.org/email
https://sagefy.org/password
`)
) // Add more routes as they are available

function ensureJwt(req, res, next) {
  // if (!req.cookies.jwt) res.cookies(...) expires, httpOnly, secure...
  next()
}

app.use(ensureJwt)

function isUser(req, res, next) {
  // const { role } = jwt.decode(req.cookies.jwt).payload
  // if (!['sg_user', 'sg_admin'].includes(role)) return res.redirect('/log-in')
  return next()
}

function isAnonymous(req, res, next) {
  // const { role } = jwt.decode(req.cookies.kwt).payload
  // if (role !== 'sg_anonymous') return res.redirect('/dashboard')
  return next()
}

function handleRegular(req, res) {
  return res.render('Index', { location: req.url, cacheHash })
}

app.get('/sign-up', isAnonymous, handleRegular)

app.post('/sign-up', isAnonymous, async (req, res) => {
  const query = gql.rootNewUser
  const variables = req.body
  const xRes = await gqlRequest({ query, variables })
  const formErrors = getFormErrors(xRes)
  if (Object.keys(formErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      formErrors,
      prevValues: req.body,
    })
  }
  return res.redirect('/dashboard') // todo set jwt
})

app.get('/log-in', isAnonymous, handleRegular)

app.post('/log-in', isAnonymous, async (req, res) => {
  const query = 'TODO'
  const variables = req.body
  const xRes = await gqlRequest({ query, variables })
  const formErrors = getFormErrors(xRes)
  if (Object.keys(formErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      formErrors,
      prevValues: req.body,
    })
  }
  return res.redirect('/dashboard') // todo set jwt
})

app.post('/email', async (req, res) => {
  const query = 'TODO'
  const variables = req.body
  const xRes = await gqlRequest({ query, variables })
  const formErrors = getFormErrors(xRes)
  if (Object.keys(formErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      formErrors,
      prevValues: req.body,
    })
  }
  return res.redirect('TODO') // then is conditional
})

app.post('/password', async (req, res) => {
  const query = 'TODO'
  const variables = req.body
  const xRes = await gqlRequest({ query, variables })
  const formErrors = getFormErrors(xRes)
  if (Object.keys(formErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      formErrors,
      prevValues: req.body,
    })
  }
  return res.redirect('TODO') // then is conditional
})

app.get('/settings', isUser, handleRegular)

app.post('/settings', isUser, async (req, res) => {
  const query = 'TODO'
  const variables = req.body
  const xRes = await gqlRequest({ query, variables })
  const formErrors = getFormErrors(xRes)
  if (Object.keys(formErrors).length) {
    return res.render('Index', {
      location: req.url,
      cacheHash,
      formErrors,
      prevValues: req.body,
    })
  }
  return res.redirect('/dashboard')
})

app.get('/log-out', isUser, (req, res) => res.clearCookie('jwt').redirect('/'))

app.get('/dashboard', isUser, handleRegular)

// For pages that don't have specific data requirements
// and don't require being logged in or logged out
// Contact, Email, Home, NotFound, Password, Search Subjects,
// Server Error, Terms
app.get('*', handleRegular)

// See express-async-errors
app.use((err, req, res, next) => {
  if (err) res.redirect('/server-error')
  next(err)
})

app.listen(process.env.PORT || 5984)

module.exports = app
