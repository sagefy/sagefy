broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .menu__overlay, .menu__trigger, .menu__item a': (e, el) ->
        e.preventDefault() if e
        tasks.toggleMenu()

    'click [href="#log_out"]': (e, el) ->
        e.preventDefault() if e
        tasks.logOutUser()
})
