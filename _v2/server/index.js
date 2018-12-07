const express = require('express')
const { postgraphile } = require('postgraphile')
const uuidv4 = require('uuid/v4')
const mailer = require('./mail')

const app = express()

app.get('/', (req, res) =>
  res.json({ message: 'Welcome to the Sagefy service!' })
)
app.get('/s', (req, res) =>
  res.json({ message: 'Welcome to the Sagefy service!' })
)

app.use(
  postgraphile(
    {
      user: 'sg_postgraphile',
      host: 'postgres',
      database: 'sagefy',
      password: 'xyz', // todo fix
      port: 5432,
    },
    'sg_public',
    {
      // Dev, debug, test
      graphiql: true,

      // JWT Authentication
      jwtSecret: uuidv4(),
      defaultRole: 'sg_anonymous',
      token: 'sg_public.jwt_token',
    }
  )
)

mailer(client)

app.listen(process.env.PORT || 8653)
