/*
Auxiliaries are utlity functions that are specific to Sagefy.
*/

const cookie = require('./cookie')
const { extend, copy, isString, isArray } = require('./utilities')

// Determine if the user is logged in
const isLoggedIn = () => cookie.get('logged_in') === '1'

// Capitalizes the first letter of a string
const ucfirst = (str = '') => str.charAt(0).toUpperCase() + str.slice(1)

// Turns underscore or camel into title case
const titleize = (str = '') => underscored(str).split('_').map(
  w => w.charAt(0).toUpperCase() + w.substr(1)
).join(' ')

// Replaces dashes and spaces with underscores, ready to be used in an URL
const underscored = str => str.replace(/[-\s]+/g, '_').toLowerCase()

// From Handlebars
const escape = (str) => {
  const chars = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '`': '&#x60;',
  }

  return str.toString().replace(/[&<>"'`]/g, char => chars[char])
}

// From http://ejohn.org/files/pretty.js
// TODO-3 move copy to content directory
const timeAgo = (str) => {
  const diff = new Date().getTime() - new Date(str).getTime()
  const days = Math.floor(diff / (24 * 60 * 60 * 1000))
  const hours = Math.floor(diff / (60 * 60 * 1000))
  const minutes = Math.floor(diff / (60 * 1000))
  if (days > 1) return `${days} days ago`
  if (days === 1) return 'Yesterday'
  if (hours > 1) return `${hours} hours ago`
  if (hours === 1) return '1 hour ago'
  if (minutes > 1) return `${minutes} minutes ago`
  if (minutes === 1) return '1 minute ago'
  return 'Just now'
}

// Return a variable friendly name of the title.
const slugify = s => s.toLowerCase().replace(/[-\s]+/g, '_')

// Set the page title.
const setTitle = (title = 'FIX ME') => {
  title = `${title} – Sagefy`
  if (typeof document !== 'undefined' && document.title !== title) {
    document.title = title
  }
}

// Wait for function to stop being called for `delay`
// milliseconds, and then finally call the real function.
const debounce = function debounce(fn, delay) {
  let timer = null
  return function debounceInternal(...args) {
    clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

// Determine if a given path matches this router.
// Returns either false or array, where array is matches parameters.
const matchesRoute = (docPath, viewPath) => {
  if (!docPath) {
    return false
  }
  docPath = docPath.split('?')[0] // Only match the pre-query params
  if (isString(viewPath)) {
    viewPath = new RegExp(
      `^${viewPath.replace(/\{([\d\w\-_\$]+)\}/g, '([^/]+)')}$`
    )
  }
  const match = docPath.match(viewPath)
  return match ? match.slice(1) : false
}

const valuefy = (value) => {
  if (typeof value === 'undefined') return undefined
  if (value === 'true') return true
  if (value === 'false') return false
  if (value === 'null') return null
  if (value.match(/^\d+\.\d+$/)) return parseFloat(value)
  if (value.match(/^\d+$/)) return parseInt(value)
  return decodeURIComponent(value)
}

const truncate = (str, len) => {
  if (str.length <= len) return str
  return `${str.slice(0, len)}...`
}

const compact = (A) => {
  const _ = []
  for (const a of A) {
    if (a) {
      _.push(a)
    }
  }
  return _
}

const mergeArraysByKey = (A, B, key = 'id') => {
  let a = 0
  let b = 0
  const C = []

  A = compact(A)
  B = compact(B)

  while (a < A.length) {
    let b2 = b
    let found = false

    while (b2 < B.length) {
      if (A[a][key] === B[b2][key]) {
        while (b <= b2) {
          C.push(B[b])
          b++
        }
        found = true
        break
      }
      b2++
    }

    if (!found) {
      C.push(A[a])
    }

    a++
  }

  while (b < B.length) {
    C.push(B[b])
    b++
  }

  return C
}

// Returns an object of the fields' value
const getFormValues = (form) => {
  const data = {}
  const forEach = (nl, fn) => Array.prototype.forEach.call(nl, fn)
  forEach(
    form.querySelectorAll(
    [
      'input[type="text"]',
      'input[type="email"]',
      'input[type="password"]',
      'input[type="hidden"]',
      'textarea',
    ].join(', ')
    ),
    (el) => {
      data[el.name] = valuefy(el.value)
    }
  )
  forEach(form.querySelectorAll('[type=radio]'), (el) => {
    if (el.checked) {
      data[el.name] = valuefy(el.value)
    }
  })
  forEach(form.querySelectorAll('[type=checkbox]'), (el) => {
    data[el.name] = data[el.name] || []
    if (el.checked) {
      data[el.name].push(valuefy(el.value))
    }
  })
  return data
}

// Given a forms values as an object, parse any fields with `.`
// in them to create a save-able object for the service
const parseFormValues = (data) => {
  const output = {}
  for (const key in data) {
    const value = data[key]
    if (key.indexOf('.') === -1) {
      output[key] = value
    } else {
      let prev = output
      let next
      const names = key
        .split('.')
        .map(n => /^\d+$/.test(n) ? parseInt(n) : n)
      names.forEach((name, i) => {
        if (i === names.length - 1) {
          prev[name] = value
        } else {
          next = names[i + 1]
          if (typeof next === 'string') {
            prev[name] = prev[name] || {}
          } else if (typeof next === 'number') {
            prev[name] = prev[name] || []
          }
          prev = prev[name]
        }
      })
    }
  }
  return output
}

// Validate the entry with the given ID against the schema.
// Returns a list of errors.
// Use this method for any sort of `create` or `update` call.
const validateFormData = (data, schema, fields) => {
  const errors = []
  ;(fields || Object.keys(schema)).forEach((fieldName) => {
    schema[fieldName].validations.forEach((fn) => {
      let error
      if (isArray(fn)) {
        error = fn[0](data[fieldName], ...fn.slice(1))
      } else {
        error = fn(data[fieldName])
      }
      if (error) {
        errors.push({
          name: fieldName,
          message: error,
        })
        return
      }
    })
  })
  return errors
}

// Given a schema, fields, errors, formData, and sending boolean (optional)
// create a list of fields with all the data needed to create the form
// correctly.
function createFieldsData({
  schema,
  fields,
  errors = [],
  formData = {},
  sending = false,
}) {
  fields = copy(fields)

  fields.forEach((field, i) => {
    fields[i] = extend({}, schema[field.name] || {}, field)
  })

  if (errors) {
    errors.forEach((error) => {
      let field = fields.filter(f => f.name === error.name)
      if (field) {
        field = field[0]
      }
      if (field) {
        field.error = error.message
      }
    })
  }

  Object.keys(formData).forEach((name) => {
    const value = formData[name]
    // All of this for the list input type
    const matches = name.match(/^(.*)\.(\d+)\.(.*)$/)
    if (matches) {
      const [, pre, index, col] = matches
      let field = fields.filter(f => f.name === pre)
      if (field) {
        field = field[0]
      }
      if (field) {
        field.value = field.value || []
        field.value[index] = field.value[index] || {}
        field.value[index][col] = value
      }
      // For every other kind of field...
    } else {
      let field = fields.filter(f => f.name === name)
      if (field) {
        field = field[0]
      }
      if (field) {
        field.value = value
      }
    }
  })

  if (sending) {
    let field = fields.filter(f => f.type === 'submit')
    if (field) {
      field = field[0]
    }
    if (field) {
      field.disabled = true
    }
  }

  return fields
}

function findGlobalErrors({ fields, errors }) {
  const fieldNames = fields.map(field => field.name)
  return errors.filter(
    error => !error.name || fieldNames.indexOf(error.name) === -1
  )
}

const prefixObjectKeys = (prefix, obj) => {
  const next = {}
  Object.keys(obj).forEach((name) => {
    const value = obj[name]
    next[prefix + name] = value
  })
  return next
}

module.exports = {
  isLoggedIn,
  ucfirst,
  titleize,
  underscored,
  escape,
  timeAgo,
  slugify,
  setTitle,
  debounce,
  matchesRoute,
  truncate,
  mergeArraysByKey,
  valuefy,

  getFormValues,
  parseFormValues,
  validateFormData,
  createFieldsData,
  findGlobalErrors,

  prefixObjectKeys,
  compact,
}
