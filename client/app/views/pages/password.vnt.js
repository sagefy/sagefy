const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')
const { getFormValues, parseFormValues } = require('../../helpers/forms')
const qs = require('../../helpers/query_string')
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
    const { token, id } = qs.read()
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
