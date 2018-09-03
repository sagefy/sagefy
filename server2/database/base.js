const { Pool } = require('pg')
const { get, mapValues } = require('lodash')
const config = require('../config')
const { convertToSlug, convertToUuid } = require('../helpers/uuidSlug')

const pool = new Pool(config.pg)

const PARAMS_REGEX = /\$[\w_]+/g

function convertValueToUuid(key, value) {
  if (key === 'id' || key.endsWith('_id')) return convertToUuid(value)
  if (key.endsWith('_ids')) return value.map(convertToUuid)
  return value
}

function convertValueToSlug(key, value) {
  if (key === 'id' || key.endsWith('_id')) return convertToSlug(value)
  if (key.endsWith('_ids')) return value.map(convertToSlug)
  return value
}

function convertText(text) {
  let count = 0
  return text.replace(PARAMS_REGEX, () => {
    count += 1
    return `$${count}`
  })
}

function convertParams(text, params) {
  const keys = text.match(PARAMS_REGEX).map(n => n.substring(1))
  return keys.map(key => convertValueToUuid(key, params[key]))
}

function convertRow(row) {
  if (!row) return row
  return mapValues(row, (value, key) => convertValueToSlug(key, value))
}

async function query(text, params) {
  const result = await pool.query(
    convertText(text),
    convertParams(text, params)
  )
  return result
}

async function saveList(text, params) {
  const res = await query(text, params)
  return res.rows.map(convertRow)
}

async function save(text, params) {
  const res = await query(text, params)
  return convertRow(get(res.rows, 0))
}

async function list(text, params) {
  try {
    return await saveList(text, params)
  } catch (e) {
    return null
  }
}

async function getOne(text, params) {
  try {
    return await save(text, params)
  } catch (e) {
    return null
  }
}

module.exports = {
  pool,
  convertValueToUuid,
  convertValueToSlug,
  convertText,
  convertParams,
  convertRow,
  query,
  saveList,
  save,
  list,
  get: getOne,
}
