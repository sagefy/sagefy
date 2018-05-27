const isString = require('lodash.isstring')
const { convertDataToGet } = require('./utilities')

// Try to parse a string as JSON, otherwise just return the string.
function parseJSON(str) {
  try {
    return JSON.parse(str)
  } catch (e) {
    return str
  }
}

// Try to parse the errors array or just return the error text.
function parseAjaxErrors(response) {
  if (!response.responseText) {
    return null
  }
  const errors = parseJSON(response.responseText)
  if (isString(errors)) {
    return errors
  }
  return errors.errors
}

module.exports = function ajax({ method, url, data }) {
  method = method.toUpperCase()
  if (method === 'GET') {
    url = convertDataToGet(url, data)
  }
  const request = new XMLHttpRequest()
  request.open(method, url, true)
  request.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
  const promise = new Promise((resolve, reject) => {
    request.onload = function onload() {
      if (this.status < 400 && this.status >= 200) {
        resolve(parseJSON(this.responseText))
      } else {
        reject(parseAjaxErrors(this))
      }
    }
    request.onerror = function onerror() {
      reject(Error())
    }
  })
  if (method === 'GET') {
    request.send()
  } else {
    request.send(JSON.stringify(data || {}))
  }
  return promise
}
