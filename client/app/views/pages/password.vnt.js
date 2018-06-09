const { getFormValues, parseFormValues } = require('../../helpers/forms')
const { readQueryString } = require('../../helpers/url')
const userSchema = require('../../schemas/user')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'submit #password.email form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      let values = getFormValues(el)
      getTasks().updateFormData(values)
      const errors = getTasks().validateForm(values, userSchema, ['email'])
      if (errors && errors.length) {
        return
      }
      values = parseFormValues(values)
      getTasks().getUserPasswordToken(values)
    },

    'submit #password.password form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const { token, id } = readQueryString()
      let values = getFormValues(el)
      values.token = token
      values.id = id
      getTasks().updateFormData(values)
      const errors = getTasks().validateForm(values, userSchema, ['password'])
      if (errors && errors.length) {
        return
      }
      values = parseFormValues(values)
      getTasks().createUserPassword(values)
    },
  })
}
