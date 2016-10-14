/*
Validations are functions which return string if there's an issue
or a nothing if okay.
*/

const util = require('../modules/utilities')
const c = require('../modules/content').get

const isBlank = val =>
    val === null || val === undefined ||
       (util.isString(val) && val === '')

// Validation functions should return a string on error,
// or return nothing if there is no problem.

// Require there to be content.
const required = (val) => {
    if (isBlank(val)) { return c('required') }
}

// Require the field to be an email address if value is present.
const email = (val) => {
    if (!isBlank(val) && (
        !util.isString(val) ||
        !val.match(/^\S+@\S+\.\S+$/)
    )) {
        return c('email')
    }
}

// Require the field to contain a minimum length if value is present.
const minlength = (val, len) => {
    if (!isBlank(val) && (
        (util.isString(val) || util.isArray(val)) &&
        val.length < len
    )) {
        return c('minlength').replace('{length}', len)
    }
}

// Require the value to be one of defined options
const isOneOf = (val, ...opts) => {
    if (!isBlank(val) && opts.indexOf(val) === -1) {
        return c('options').replace('{options}', opts.join(' '))
    }
}

module.exports = {required, email, minlength, isOneOf}
