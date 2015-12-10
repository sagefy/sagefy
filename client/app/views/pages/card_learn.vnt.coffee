broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click #card-learn .continue': (e, el) ->
        e.preventDefault if e
        container = closest(el, document.body, '#card-learn')
        if 'video' in container.className
            data = {}
        tasks.respondToCard(el.id, data)
        # TODO@ unless positive feedback already received...
})
