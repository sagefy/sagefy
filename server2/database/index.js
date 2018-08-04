const { Pool } = require('pg')
const get = require('lodash.get')
const config = require('../config')

const pool = new Pool(config.pg)

function query(text, params) {
  return pool.query(text, params)
}

async function list(text, params) {
  try {
    const res = await query(text, params)
    return res.rows
  } catch (e) {
    return null
  }
}

async function getOne(text, params) {
  const rows = await list(text, params)
  return get(rows, 0)
}

module.exports = {
  query,
  list,
  getOne,
}
