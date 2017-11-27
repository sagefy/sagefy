const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const { closest } = require('../../modules/utilities')

module.exports = broker.add({
  'click .choose-unit__engage'(e, el) {
    if (e) {
      e.preventDefault()
    }
    const ul = closest(el, 'ul')
    tasks.chooseUnit(ul.id, el.id)
  },
})
