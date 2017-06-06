const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .menu__overlay, .menu__trigger, .menu__item a'(e) {
        if(e) { e.preventDefault() }
        tasks.toggleMenu()
    },

    'click [href="#log_out"]'(e) {
        if(e) { e.preventDefault() }
        tasks.logOutUser()
    },
})
