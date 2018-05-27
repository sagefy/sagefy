/*
Utilities are one-off functions that are used throughout the framework.
*/
const merge = require('lodash.merge')

const util = {}

// Test for types.
;['Object', 'Array', 'Function', 'Date', 'String', 'RegExp'].forEach(type => {
  util[`is${type}`] = a =>
    Object.prototype.toString.call(a) === `[object ${type}]`
})

const objectConstructor = {}.constructor
util.isPlainObject = function isPlainObject(val) {
  return val.constructor === objectConstructor
}

util.isUndefined = a => typeof a === 'undefined'

// http://stackoverflow.com/a/9716488
util.isNumber = n => !Number.isNaN(parseFloat(n)) && Number.isFinite(n)

// Makes a copy of the array or object.
util.copy = obj => {
  if (util.isObject(obj)) {
    return merge({}, obj)
  }
  if (util.isArray(obj)) {
    return merge([], obj)
  }
  if (util.isDate(obj)) {
    return new Date(obj)
  }
  return obj
}

util.shallowCopy = obj =>
  Object.keys(obj).reduce((next, key) => {
    next[key] = obj[key]
    return next
  }, {})

// Try to parse a string as JSON, otherwise just return the string.
util.parseJSON = str => {
  try {
    return JSON.parse(str)
  } catch (e) {
    return str
  }
}

// Find the closest element matching the given selector.
require('./matches_polyfill')

util.closest = (element, selector, top = document.body) => {
  while (!element.matches(selector)) {
    element = element.parentNode
    if (element === top) {
      return null
    }
  }
  return element
}

// Convert an object to a query string for GET requests.
util.parameterize = obj => {
  obj = util.copy(obj)
  const pairs = []
  Object.keys(obj).forEach(key => {
    const value = obj[key]
    pairs.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
  })
  return pairs.join('&').replace(/%20/g, '+')
}

util.convertDataToGet = (url, data) => {
  url += url.indexOf('?') > -1 ? '&' : '?'
  url += util.parameterize(
    merge(
      data || {},
      { _: +new Date() } // Cachebreaker
    )
  )
  return url
}

util.flatten = function flatten(arr) {
  return arr.reduce(
    (acc, val) => acc.concat(Array.isArray(val) ? flatten(val) : val),
    []
  )
}

util.omit = function omit(o, keys) {
  return Object.keys(o).reduce((sum, key) => {
    if (keys.indexOf(key) === -1) {
      sum[key] = o[key]
    }
    return sum
  }, {})
}

module.exports = util
