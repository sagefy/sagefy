/*
Utilities are one-off functions that are used throughout the framework.
*/
const merge = require('lodash.merge')
const cloneDeep = require('lodash.clonedeep')

// Find the closest element matching the given selector.
require('./matches_polyfill')

function closest(element, selector, top = document.body) {
  while (!element.matches(selector)) {
    element = element.parentNode
    if (element === top) {
      return null
    }
  }
  return element
}

// Convert an object to a query string for GET requests.
function parameterize(obj) {
  obj = cloneDeep(obj)
  const pairs = []
  Object.keys(obj).forEach(key => {
    const value = obj[key]
    pairs.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
  })
  return pairs.join('&').replace(/%20/g, '+')
}

function convertDataToGet(url, data) {
  url += url.indexOf('?') > -1 ? '&' : '?'
  url += parameterize(
    merge(
      data || {},
      { _: +new Date() } // Cachebreaker
    )
  )
  return url
}

module.exports = {
  closest,
  parameterize,
  convertDataToGet,
}
