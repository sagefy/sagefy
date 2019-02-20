const express = require('express')
const { postgraphile } = require('postgraphile')
const uuidv4 = require('uuid/v4')
require('dotenv').config()

require('./mail')()

const app = express()

app.get('/', (req, res) =>
  res.json({ message: 'Welcome to the Sagefy service!' })
)

app.get('/x', (req, res) =>
  res.json({ message: 'Welcome to the Sagefy service!' })
)

app.use(
  postgraphile(
    {
      user: process.env.DB_USER || 'sg_postgraphile',
      host: process.env.DB_HOST || 'postgres',
      database: process.env.DB_DATABASE || 'sagefy',
      password: process.env.DB_PASSWORD,
      port: process.env.DB_PORT || 5432,
    },
    process.env.DB_SCHEMA || 'sg_public',
    {
      // Dev, debug, test
      graphiql: true,

      // JWT Authentication
      jwtSecret: process.env.JWT_SECRET || uuidv4(),
      defaultRole: process.env.JWT_ROLE || 'sg_anonymous',
      jwtPgTypeIdentifier: process.env.JWT_TOKEN || 'sg_public.jwt_token',
    }
  )
)

app.listen(process.env.SERVER_PORT || 8653)
