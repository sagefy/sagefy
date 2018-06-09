/* eslint-disable no-console */
const express = require('express')
const { render } = require('ultradom')
const { JSDOM } = require('jsdom')
const template = require('./views/index.tmpl')
const { route } = require('./helpers/route_actions')
const createStore = require('./helpers/store')
const reducer = require('./reducers/index')
const cookieParser = require('cookie-parser')
const addAllTasks = require('./tasks/index')

const app = express()
app.use(cookieParser())

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

function toHTML(node) {
  const dom = new JSDOM('<body></body>')
  const { document } = dom.window
  global.document = document
  render(node, document.body)
  return document.body.innerHTML
}

function renderHtml(store) {
  const state = store.getState()
  return html
    .replace('{title}', state.routeTitle)
    .replace('{body}', toHTML(template(state)))
    .replace('{state}', JSON.stringify(state))
}

app.get(/.*/, (request, response) => {
  const path = request.originalUrl
  console.log(path)
  // !!! make sure the store doesn't use a pre-existing state !!!
  const store = createStore()
  store.setReducer(reducer)
  store.requestCookie = `session_id=${request.cookies.session_id}`
  addAllTasks(store)
  const promise = route(store, path)
  if (promise) {
    promise
      .then(() => {
        response.status(200).send(renderHtml(store))
      })
      .catch(error => {
        console.error(error)
      })
  } else {
    response.status(200).send(renderHtml(store))
  }
})

app.listen(5984, () => {
  console.log('serving app realness')
})
