/* eslint-disable no-console, global-require */

const fs = require('fs').promises

async function setup() {
  console.log('Running setup...')
  // This require brings in Postgraphile...
  // So give it some time to run.
  const { pool } = require('../index')
  pool.on('error', console.error)
  // We'll generate our dev/test data first...
  const data = await require('./_dev-data')()
  // As bizarre as this is, this is the only way to
  // pass along data from the setup phase to the test phase.
  await fs.writeFile('test-data.json', JSON.stringify(data), 'utf8')
  console.log('Finished setup.')
}

module.exports = setup
