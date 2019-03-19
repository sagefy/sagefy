/* eslint-disable security/detect-non-literal-fs-filename */
const fs = require('fs')
const fromPairs = require('lodash.frompairs')
const get = require('lodash.get')
const gqlRequest = require('./gql-request')

const JWT_COOKIE_NAME = 'jwt'

function convertDashToCamel(str) {
  return str.replace(/-([a-z])/g, g => g[1].toUpperCase())
}

module.exports = fromPairs(
  fs.readdirSync('./graphql').map(filename => [
    convertDashToCamel(
      filename.replace('./graphql/', '').replace('.graphql', '')
    ),
    req =>
      gqlRequest({
        query: fs.readFileSync(`./graphql/${filename}`, 'utf8'),
        variables: req.body,
        jwtToken: get(req.cookies, JWT_COOKIE_NAME),
      }),
  ])
)