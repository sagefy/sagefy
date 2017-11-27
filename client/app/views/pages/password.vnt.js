const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const { getFormValues, parseFormValues } = require('../../modules/auxiliaries')
const qs = require('../../modules/query_string')
const userSchema = require('../../schemas/user')

module.exports = broker.add({
  'submit #password.email form'(e, el) {
    if (e) {
      e.preventDefault()
    }
    let values = getFormValues(el)
    tasks.updateFormData(values)
    const errors = tasks.validateForm(values, userSchema, ['email'])
    if (errors && errors.length) {
      return
    }
    values = parseFormValues(values)
    tasks.getUserPasswordToken(values)
  },

  'submit #password.password form'(e, el) {
    if (e) {
      e.preventDefault()
    }
    const { token, id } = qs.get()
    let values = getFormValues(el)
    values.token = token
    values.id = id
    tasks.updateFormData(values)
    const errors = tasks.validateForm(values, userSchema, ['password'])
    if (errors && errors.length) {
      return
    }
    values = parseFormValues(values)
    tasks.createUserPassword(values)
  },
})
