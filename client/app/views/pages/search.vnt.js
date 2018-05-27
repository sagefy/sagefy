const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')
const { closest } = require('../../helpers/utilities')

module.exports = broker.add({
  'click #search [type="submit"]'(e, el) {
    if (e) {
      e.preventDefault()
    }
    const form = closest(el, 'form')
    const input = form.querySelector('input')
    tasks.search({ q: input.value })
  },

  'click .add-to-my-subjects'(e, el) {
    if (e) {
      e.preventDefault()
    }
    tasks.addUserSubject(el.id)
  },
})
