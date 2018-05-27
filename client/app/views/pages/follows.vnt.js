/* eslint-disable no-alert */
const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')

module.exports = broker.add({
  'click .follows__unfollow-button'(e, el) {
    if (e) {
      e.preventDefault()
    }
    // TODO-2 switch to undo
    if (window.confirm('Unfollow?')) {
      tasks.unfollow(el.id)
    }
  },
})
