const get = require('lodash.get')
const mapValues = require('lodash.mapvalues')
const { parse, stringify } = require('query-string')
const valuefy = require('./valuefy')

function readQueryString(string) {
  string = string || (typeof window !== 'undefined' && window.location.search)
  return mapValues(parse(string), valuefy)
}

function writeGetUrl(url, data) {
  return (
    url +
    (url.indexOf('?') > -1 ? '&' : '?') +
    stringify(Object.assign({ _: Date.now() }, data))
  )
}

// Try to parse a string as JSON, otherwise just return the string.
function parseJSON(str) {
  try {
    return JSON.parse(str)
  } catch (e) {
    return str
  }
}

// Try to parse the errors array or just return the error text.
function parseAjaxErrors(str) {
  const response = parseJSON(str)
  return get(response, 'errors', response)
}

module.exports = {
  readQueryString,
  writeGetUrl,
  parseJSON,
  parseAjaxErrors,
}
