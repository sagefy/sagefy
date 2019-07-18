/* eslint-disable security/detect-non-literal-fs-filename */
const fs = require('fs')
const fromPairs = require('lodash.frompairs')
const get = require('lodash.get')
const { GraphQLClient } = require('graphql-request')

const JWT_COOKIE_NAME = 'jwt'
const ENDPOINT = 'http://server:2601/graphql'

function convertDashToCamel(str) {
  return str.replace(/-([a-z])/g, g => g[1].toUpperCase())
}

function convertGqlFileToQueryName(filename) {
  return convertDashToCamel(filename.replace(/^(.*?)\.graphql$/, '$1'))
}

function getJwtToken(req) {
  return get(req.cookies, JWT_COOKIE_NAME)
}

function makeGraphQLRequest(query) {
  return (req, variables) => {
    const jwtToken = getJwtToken(req)
    const options = { headers: {} }
    if (jwtToken) options.headers.Authorization = `Bearer ${jwtToken}`
    const graphQLClient = new GraphQLClient(ENDPOINT, options)
    return graphQLClient.request(query, variables)
  }
}

const queries = fromPairs(
  fs
    .readdirSync('./graphql')
    .map(filename => [
      convertGqlFileToQueryName(filename),
      fs.readFileSync(`./graphql/${filename}`, 'utf8'),
    ])
    .map(([queryName, query]) => [queryName, makeGraphQLRequest(query)])
)

module.exports = queries
