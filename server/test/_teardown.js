/* eslint-disable no-console */
const { pool } = require('../index')

async function teardown() {
  console.log('Tearing down...')
  await pool.end()
  console.log('Torn down.')
}

module.exports = teardown
