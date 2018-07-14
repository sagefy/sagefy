/* eslint-disable no-console */
import express from 'express'
import cookieParser from 'cookie-parser'

import React from 'react'
import { Provider } from 'react-redux'
import ReactDOMServer from 'react-dom/server'
import { StaticRouter as Router } from 'react-router-dom'

import Index from './views/Index'
import createSagefyStore from './helpers/createStore'

const app = express()
app.use(cookieParser())

const html = `
<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – Sagefy</title>
<link href="https://fonts.googleapis.com/css?family=Rubik:400,400i,500,500i" rel="stylesheet">
<link rel="stylesheet" href="/index2.css?___">
<body>
<div class="vdom">{innerHtml}</div>
<script>window.preload={state}</script>
<script src="https://cdn.polyfill.io/v2/polyfill.min.js"></script>
<script src="/index2.js?___"></script>
</body>
`
  .replace('{title}', '')
  .replace('{body}', '')
  .replace('{state}', 'null')
  .replace(/\n/g, '')
  .replace(/___/g, Date.now())

app.get(/.*/, (request, response) => {
  const path = request.originalUrl
  console.log('Serving HTML realness on: ', path)
  // !!! make sure the store doesn't use a pre-existing state !!!
  const myContext = {}
  const store = createSagefyStore()
  const innerHtml = ReactDOMServer.renderToString(
    <Provider store={store}>
      <Router location={request.url} context={myContext}>
        <Index />
      </Router>
    </Provider>
  )
  if (myContext.url) {
    response.redirect(myContext.url)
  } else {
    response.status(200).send(html.replace('{innerHtml}', innerHtml))
  }
})

app.listen(5985, () => {
  console.log('serving app realness')
})
