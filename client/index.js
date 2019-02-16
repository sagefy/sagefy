const path = require('path')
const express = require('express')
const request = require('./request')

const app = express()

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
  try {
    const xRes = await request(body)
    return res.send(xRes)
  } catch (e) {
    return res.status(500).send(e)
  }

  // If worked... return res.redirect('/dashboard')
  // If failed... return res.redirect('back')
})

// For pages that don't have specific data requirements
app.get('*', (req, res) => res.render('Index', { location: req.url }))

app.listen(process.env.PORT || 5984)

module.exports = app
