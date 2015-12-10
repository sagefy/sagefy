broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click #card-learn .continue': (e, el) ->
        e.preventDefault if e
        tasks.respondToCard(id, data)
        # TODO@ unless positive feedback already received...
})
