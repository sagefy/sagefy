broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    'click .tree circle': (e, el) ->
        e.preventDefault() if e
        if el.classList.contains('selected')
            actions.selectTreeUnit()
        else
            actions.selectTreeUnit(el.id)

    'click .tree text': (e, el) ->
        e.preventDefault() if e
        actions.selectTreeUnit()
})
