const { getFormValues, parseFormValues } = require('../../helpers/forms')
const userSchema = require('../../schemas/user')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'submit #sign-up form'(e, el) {
      if (e) e.preventDefault()
      let values = getFormValues(el)
      getTasks().updateFormData(values)
      const errors = getTasks().validateForm(values, userSchema, [
        'name',
        'email',
        'password',
      ])
      if (errors && errors.length) {
        return
      }
      values = parseFormValues(values)
      getTasks().createUser(values)
    },
  })
}
