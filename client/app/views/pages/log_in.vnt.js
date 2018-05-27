const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')
const { getFormValues, parseFormValues } = require('../../helpers/forms')
const userSchema = require('../../schemas/user')

module.exports = broker.add({
  'submit #log-in form'(e, el) {
    if (e) {
      e.preventDefault()
    }
    let values = getFormValues(el)
    tasks.updateFormData(values)
    const errors = tasks.validateForm(values, userSchema, ['name', 'password'])
    if (errors && errors.length) {
      return
    }
    values = parseFormValues(values)
    tasks.logInUser(values)
  },
})
