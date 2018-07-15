/* eslint-disable no-console */

const express = require('express')
const morgan = require('morgan')

const indexRoutes = require('./routes/index')

const app = express()
app.use(morgan('tiny'))
indexRoutes(app)
app.listen(8654, () => console.log('Listening on port 8654.'))

// https://gist.github.com/zerbfra/70b155fa00b4e0d6fd1d4e090a039ad4
