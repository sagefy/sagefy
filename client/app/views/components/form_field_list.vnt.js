const closest = require('../../helpers/closest')
const { getFormValues } = require('../../helpers/forms')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .form-field--list__remove-row'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const form = closest(el, 'form')
      const values = getFormValues(form)
      const table = closest(el, 'table')
      const { name } = table.dataset
      const index = parseInt(el.dataset.index, 10)
      getTasks().removeListFieldRow(values, name, index)
    },

    'click .form-field--list__add-row'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const form = closest(el, 'form')
      const values = getFormValues(form)
      const table = closest(el, 'table')
      const { name } = table.dataset
      const columns = Array.prototype.map
        .call(table.querySelectorAll('th'), xel => xel.dataset.col)
        .filter(c => c)
      getTasks().addListFieldRow(values, name, columns)
    },

    // TODO-3 'dragstart .form-field--list__move-row'(e, el)
    // TODO-3 'drop form-field--list__move-row'(e, el)
  })
}
