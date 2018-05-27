/* eslint-disable no-console */
const express = require('express')
const toHTML = require('snabbdom-to-html')
const template = require('./views/index.tmpl')
const { route } = require('./helpers/route_actions')
const { getState, setReducer, resetState } = require('./helpers/store')
const reducer = require('./reducers/index')
const cookieParser = require('cookie-parser')

// Require all tasks
require('./tasks/index')

const app = express()
app.use(cookieParser())

setReducer(reducer)

const html = `
<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – Sagefy</title>
<link href="https://fonts.googleapis.com/css?family=Rubik:400,400i,500,500i" rel="stylesheet">
<link rel="stylesheet" href="/index.css?___">
<body>{body}
<script>window.preload={state}</script>
<script src="https://cdn.polyfill.io/v2/polyfill.min.js"></script>
<script src="/index.js?___"></script>
</body>
`
  .replace(/\n/g, '')
  .replace(/___/g, Date.now())

function render() {
  const state = getState()
  return html
    .replace('{title}', state.routeTitle)
    .replace('{body}', toHTML(template(state)))
    .replace('{state}', JSON.stringify(state))
}

app.get(/.*/, (request, response) => {
  const path = request.originalUrl
  console.log(path)
  resetState() // make sure it doesn't use a pre-existing state
  global.requestCookie = `session_id=${request.cookies.session_id}`
  const promise = route(path)
  if (promise) {
    promise
      .then(() => {
        response.status(200).send(render())
      })
      .catch(error => {
        console.error(error)
      })
  } else {
    response.status(200).send(render())
  }
})

app.listen(5984, () => {
  console.log('serving app realness')
})
