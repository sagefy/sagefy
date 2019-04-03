/* eslint-disable security/detect-non-literal-fs-filename, global-require, import/no-extraneous-dependencies */
const fs = require('fs')
const fromPairs = require('lodash.frompairs')
const request = require('supertest')
const get = require('lodash.get')
const { app } = require('../index')

function convertDashToCamel(str) {
  return str.replace(/-([a-z])/g, g => g[1].toUpperCase())
}

const GQL = fromPairs(
  fs
    .readdirSync('../client/graphql')
    .map(filename => [
      convertDashToCamel(
        filename.replace('../client/graphql/', '').replace('.graphql', '')
      ),
      fs.readFileSync(`../client/graphql/${filename}`, 'utf8'),
    ])
)

let data
async function getData() {
  // As weird as this is,
  // its the only way to communicate from the setup to the test runner
  if (!data)
    data = JSON.parse(await fs.promises.readFile('test-data.json', 'utf8'))
  return data
}

async function getLoginToken(name) {
  const response = await request(app)
    .post('/graphql')
    .send({
      query: GQL.rootLogInUser,
      variables: {
        name,
        password: 'example1',
      },
    })
  return get(response, 'body.data.logIn.jwtToken')
}

module.exports = {
  GQL,
  getData,
  getLoginToken,
}
