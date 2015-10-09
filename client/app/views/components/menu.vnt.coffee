broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    'click .menu__overlay, .menu__trigger, .menu__item a': (e, el) ->
        e.preventDefault() if e
        actions.toggleMenu()

    'click [href="#log_out"]': (e, el) ->
        e.preventDefault() if e
        actions.logOutUser()
})
