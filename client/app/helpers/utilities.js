/*
Utilities are one-off functions that are used throughout the framework.
*/
const merge = require('lodash.merge')
const isObject = require('lodash.isobject')
const isArray = require('lodash.isarray')
const isDate = require('lodash.isdate')

const util = {}

// Makes a copy of the array or object.
util.copy = obj => {
  if (isObject(obj)) {
    return merge({}, obj)
  }
  if (isArray(obj)) {
    return merge([], obj)
  }
  if (isDate(obj)) {
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
    (acc, val) => acc.concat(isArray(val) ? flatten(val) : val),
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
