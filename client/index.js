const path = require('path')
const express = require('express')

const app = express()

app.set('views', path.join(__dirname, '/views'))
app.set('view engine', 'jsx')
app.engine('jsx', require('express-react-views').createEngine())

app.get('/sitemap', (req, res) => res.send('Do: https://sagefy.org')) // TODO

app.get('/suggest', (req, res) => {
  // TODO list all suggests
  res.render('Index', { location: req.url })
})

app.get('/search-subjects', (req, res) => {
  // TODO query all suggests
  res.render('Index', { location: req.url })
})

app.post('/suggest', (req, res) => {
  // TODO create a new suggest
  res.redirect('back')
})

app.post('/suggest:upvote', (req, res) => {
  // TODO create a suggest-follow
  res.redirect('back')
})

// For pages that don't have specific data requirements
app.get('*', (req, res) => res.render('Index', { location: req.url }))

app.listen(process.env.PORT || 5984)
