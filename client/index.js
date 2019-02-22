/* eslint-disable max-params, no-console */
const path = require('path')
const express = require('express')
const bodyParser = require('body-parser')
const get = require('lodash.get')
const request = require('./request')
const getFormErrors = require('./selectors/form-errors')

require('express-async-errors')

const cacheHash =
  process.env.NODE_ENV === 'test' ? '_' : Date.now().toString(36)

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

// For pages that don't have specific data requirements
app.get('*', (req, res) =>
  res.render('Index', { location: req.url, cacheHash })
)

// See express-async-errors
app.use((err, req, res, next) => {
  if (err) {
    res.redirect('/server-error')
  }
  next(err)
})

app.listen(process.env.PORT || 5984)

module.exports = app
