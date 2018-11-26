const express = require('express')
const { postgraphile } = require('postgraphile')

const app = express()

app.get('/', (req, res) => res.json({ message: 'Welcome to the Sagefy service!' }))
app.get('/s', (req, res) => res.json({ message: 'Welcome to the Sagefy service!' }))

app.use(postgraphile({
  user: 'sagefy',
  host: 'postgres',
  database: 'sagefy',
  // password
  port: 5432,
}, 'sg_public', {
  graphiql: true
}))

app.listen(process.env.PORT || 8653)
