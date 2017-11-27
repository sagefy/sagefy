/* eslint-disable no-alert */
const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')

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
