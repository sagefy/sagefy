/*
Validations are functions which return string if there's an issue
or a nothing if okay.
*/

const isString = require('lodash.isstring')
const isArray = require('lodash.isarray')
const c = require('../helpers/content').get

function isBlank(val) {
  return val === null || val === undefined || (isString(val) && val === '')
}

// Validation functions should return a string on error,
// or return nothing if there is no problem.

// Require there to be content.
function required(val) {
  if (isBlank(val)) {
    return c('required')
  }
  return null
}

// Require the field to be an email address if value is present.
function email(val) {
  if (!isBlank(val) && (!isString(val) || !val.match(/^\S+@\S+\.\S+$/))) {
    return c('email')
  }
  return null
}

// Require the field to contain a minimum length if value is present.
function minlength(val, len) {
  if (!isBlank(val) && ((isString(val) || isArray(val)) && val.length < len)) {
    return c('minlength').replace('{length}', len)
  }
  return null
}

// Require the value to be one of defined options
function isOneOf(val, ...opts) {
  if (!isBlank(val) && opts.indexOf(val) === -1) {
    return c('options').replace('{options}', opts.join(' '))
  }
  return null
}

module.exports = { required, email, minlength, isOneOf }
