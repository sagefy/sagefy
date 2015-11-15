broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    'click .follow': (e, el) ->
        e.preventDefault() if e
        [kind, id] = el.id.split('_')
        actions.follow({
            entity: {
                id: id
                kind: kind
            }
        })
})
