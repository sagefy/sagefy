/* eslint-disable no-console */
import express from 'express'
import cookieParser from 'cookie-parser'
import ReactDOMServer from 'react-dom/server'

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
<div class="vdom"></div>
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
  console.log(path)
  // ReactDOMServer.renderToString(element)
  // !!! make sure the store doesn't use a pre-existing state !!!
  response.status(200).send(html)
})

app.listen(5985, () => {
  console.log('serving app realness')
})
