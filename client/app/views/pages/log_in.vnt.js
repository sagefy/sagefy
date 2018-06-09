const { getFormValues, parseFormValues } = require('../../helpers/forms')
const userSchema = require('../../schemas/user')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'submit #log-in form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      let values = getFormValues(el)
      getTasks().updateFormData(values)
      const errors = getTasks().validateForm(values, userSchema, [
        'name',
        'password',
      ])
      if (errors && errors.length) {
        return
      }
      values = parseFormValues(values)
      getTasks().logInUser(values)
    },
  })
}
