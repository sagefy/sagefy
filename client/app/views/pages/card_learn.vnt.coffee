broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    '#card-learn .continue': (e, el) ->
        e.preventDefault if e
        actions.respondToCard(id, data)
        # TODO@ unless positive feedback already received...
})
