const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')

module.exports = broker.add({
  'click .menu__overlay, .menu__trigger, .menu__item a'(e) {
    if (e) {
      e.preventDefault()
    }
    tasks.toggleMenu()
  },

  'click [href="#log_out"]'(e) {
    if (e) {
      e.preventDefault()
    }
    tasks.logOutUser()
  },
})
