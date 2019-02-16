const path = require('path')
const express = require('express')
const request = require('./request')

require('express-async-errors')

const app = express()

// See https://github.com/reactjs/express-react-views#add-it-to-your-app
app.set('views', path.join(__dirname, '/views'))
app.set('view engine', 'jsx')
app.engine('jsx', require('express-react-views').createEngine())

// See express-async-errors
app.use((err, req, res, next) => {
  // eslint-disable-line max-params
  if (err) {
    console.error(err)
    res.status(500)
    res.json({ error: err.message })
  }
  next(err)
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
app.get('*', (req, res) => res.render('Index', { location: req.url }))

app.listen(process.env.PORT || 5984)

module.exports = app
