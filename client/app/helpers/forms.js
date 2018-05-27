const merge = require('lodash.merge')
const isArray = require('lodash.isarray')
const cloneDeep = require('lodash.clonedeep')
const valuefy = require('./valuefy')

// Returns an object of the fields' value
function getFormValues(form) {
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
    el => {
      data[el.name] = valuefy(el.value)
    }
  )
  forEach(form.querySelectorAll('[type=radio]'), el => {
    if (el.checked) {
      data[el.name] = valuefy(el.value)
    }
  })
  forEach(form.querySelectorAll('[type=checkbox]'), el => {
    data[el.name] = data[el.name] || []
    if (el.checked) {
      data[el.name].push(valuefy(el.value))
    }
  })
  return data
}

// Given a forms values as an object, parse any fields with `.`
// in them to create a save-able object for the service
function parseFormValues(data) {
  const output = {}
  Object.keys(data).forEach(key => {
    const value = data[key]
    if (key.indexOf('.') === -1) {
      output[key] = value
    } else {
      let prev = output
      let next
      const names = key
        .split('.')
        .map(n => (/^\d+$/.test(n) ? parseInt(n, 10) : n))
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
  })
  return output
}

// Validate the entry with the given ID against the schema.
// Returns a list of errors.
// Use this method for any sort of `create` or `update` call.
function validateFormData(data, schema, fields) {
  const errors = []
  ;(fields || Object.keys(schema)).forEach(fieldName => {
    schema[fieldName].validations.forEach(fn => {
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
  fields = cloneDeep(fields)

  fields.forEach((field, i) => {
    fields[i] = merge({}, schema[field.name] || {}, field)
  })

  if (errors) {
    errors.forEach(error => {
      let field = fields.filter(f => f.name === error.name)
      if (field) {
        ;[field] = field
      }
      if (field) {
        field.error = error.message
      }
    })
  }

  Object.keys(formData).forEach(name => {
    const value = formData[name]
    // All of this for the list input type
    const matches = name.match(/^(.*)\.(\d+)\.(.*)$/)
    if (matches) {
      const [, pre, index, col] = matches
      let field = fields.filter(f => f.name === pre)
      if (field) {
        ;[field] = field
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
        ;[field] = field
      }
      if (field) {
        field.value = value
      }
    }
  })

  if (sending) {
    let field = fields.filter(f => f.type === 'submit')
    if (field) {
      ;[field] = field
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

function prefixObjectKeys(prefix, obj) {
  const next = {}
  Object.keys(obj).forEach(name => {
    const value = obj[name]
    next[prefix + name] = value
  })
  return next
}

module.exports = {
  getFormValues,
  parseFormValues,
  validateFormData,
  createFieldsData,
  findGlobalErrors,
  prefixObjectKeys,
}
