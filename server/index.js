const express = require('express')
const { postgraphile } = require('postgraphile')
const { Pool } = require('pg')

const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.NODE_ENV === 'test' ? 'localhost' : process.env.DB_HOST,
  database: process.env.DB_DATABASE,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
})

const app = express()

app.use(
  postgraphile(pool, process.env.DB_SCHEMA, {
    // Dev, debug, test
    graphiql: process.env.NODE_ENV !== 'production',
    enhanceGraphiql: process.env.NODE_ENV !== 'production',

    // JWT Authentication
    jwtSecret: process.env.JWT_SECRET,
    defaultRole: process.env.JWT_ROLE,
    jwtPgTypeIdentifier: process.env.JWT_TOKEN,

    // Postgraphile recommended config
    setofFunctionsContainNulls: true,
    // If none of your RETURNS SETOF compound_type functions
    // mix NULLs with the results
    // then you may set this true
    // to reduce the nullables in the GraphQL schema.
    ignoreRBAC: false,
    // Exclude fields, queries and mutations that the
    // user isn't permitted to access from the generated GraphQL schema.
    ignoreIndexes: false,
    // Exclude filters, orderBy, and relations that would
    // be expensive to access due to missing indexes.
    dynamicJson: true,
    // Enables raw JSON input and output.
    legacyRelations: 'omit',

    // Production config
    disableQueryLog: process.env.NODE_ENV !== 'development',

    // Dev, Test, CI Config
    showErrorStack: process.env.NODE_ENV !== 'production',
    extendedErrors:
      process.env.NODE_ENV === 'production'
        ? []
        : ['hint', 'detail', 'errcode'],
  })
)

if (require.main === module) {
  require('./mail')() // eslint-disable-line
  app.listen(process.env.SERVER_PORT || 8653)
}

module.exports = { app, pool }
