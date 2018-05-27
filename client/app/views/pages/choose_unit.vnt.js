const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')
const { closest } = require('../../helpers/utilities')

module.exports = broker.add({
  'click .choose-unit__engage'(e, el) {
    if (e) {
      e.preventDefault()
    }
    const ul = closest(el, 'ul')
    tasks.chooseUnit(ul.id, el.id)
  },
})
