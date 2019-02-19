/* eslint-disable max-params, no-console */
const path = require('path')
const express = require('express')
const request = require('./request')

require('express-async-errors')

const cacheHash =
  process.env.NODE_ENV === 'test' ? '_' : Date.now().toString(36)

const app = express()

// See https://github.com/reactjs/express-react-views#add-it-to-your-app
app.set('views', path.join(__dirname, '/views'))
app.set('view engine', 'jsx')
app.engine('jsx', require('express-react-views').createEngine())

// See express-async-errors
app.use((err, req, res, next) => {
  if (!err) next(err)
  console.error(err)
  res.status(500)
  res.send(err.message)
})

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
  const body = `
  query {
    allSuggests {
      edges {
        node {
          id
        }
      }
    }
  }`
  const xRes = await request(body)
  return res.send(xRes)

  // If worked... return res.redirect('/dashboard')
  // If failed... return res.redirect('back')
})

// For pages that don't have specific data requirements
app.get('*', (req, res) =>
  res.render('Index', { location: req.url, cacheHash })
)

app.listen(process.env.PORT || 5984)

module.exports = app
