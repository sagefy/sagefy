const closest = require('../../helpers/closest')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click #search [type="submit"]'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const form = closest(el, 'form')
      const input = form.querySelector('input')
      getTasks().search({ q: input.value })
    },

    'click .add-to-my-subjects'(e, el) {
      if (e) {
        e.preventDefault()
      }
      getTasks().addUserSubject(el.id)
    },
  })
}
