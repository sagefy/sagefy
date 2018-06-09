const { getFormValues, parseFormValues } = require('../../helpers/forms')
const userSchema = require('../../schemas/user')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'submit #settings form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      let values = getFormValues(el)
      getTasks().updateFormData(values)
      const errors = getTasks().validateForm(values, userSchema, [
        'name',
        'email',
      ])
      if (errors && errors.length) {
        return
      }
      values = parseFormValues(values)
      getTasks().updateUser(values)
    },
  })
}
