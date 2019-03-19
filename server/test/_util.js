/* eslint-disable security/detect-non-literal-fs-filename */
const fs = require('fs')
const fromPairs = require('lodash.frompairs')

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

module.exports = {
  GQL,
}
