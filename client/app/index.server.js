const express = require('express')
const toHTML = require('vdom-to-html')
const template = require('./views/index.tmpl')
const {route} = require('./modules/route_actions')
const store = require('./modules/store')

const app = express()

const htmlTop = [
    '<!doctype html>',
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<link rel="stylesheet" href="/index.css?___">',
    '<script src="/index.js?___"></script>',
    '<body>',
].join('')

const htmlBottom = '</body>'

app.get(/.*/, (request, response) => {
    const path = request.path
    route(path)
        .then(() => {
            const state = store.data
            // currentUserId
            // route
            response.status(200).send(
                htmlTop +
                toHTML(template(state)) +
                `<script>window.preload=${JSON.stringify(state)}` +
                htmlBottom
            )
        })
})

app.listen(5984, () => {
    console.log('serving app realness') // eslint-disable-line
})
