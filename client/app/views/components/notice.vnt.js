const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')

module.exports = broker.add({
  'click .notice'(e, el) {
    if (el.classList.contains('notice--unread')) {
      tasks.markNotice(el.id)
    }
  },
})
