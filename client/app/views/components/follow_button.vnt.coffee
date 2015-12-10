broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .follow': (e, el) ->
        e.preventDefault() if e
        [kind, id] = el.id.split('_')
        tasks.follow({
            entity: {
                id: id
                kind: kind
            }
        })
})
