const express = require('express')
const { postgraphile } = require('postgraphile')
require('dotenv').config()

require('./mail')()

const app = express()

app.use(
  postgraphile(
    {
      user: process.env.DB_USER,
      host: process.env.DB_HOST,
      database: process.env.DB_DATABASE,
      password: process.env.DB_PASSWORD,
      port: process.env.DB_PORT,
    },
    process.env.DB_SCHEMA,
    {
      // Dev, debug, test
      graphiql: true,

      // JWT Authentication
      jwtSecret: process.env.JWT_SECRET,
      defaultRole: process.env.JWT_ROLE,
      jwtPgTypeIdentifier: process.env.JWT_TOKEN,
    }
  )
)

app.listen(process.env.SERVER_PORT || 8653)
