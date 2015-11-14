broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    'click #unit .follow': (e, el) ->
        e.preventDefault() if e
        actions.follow({
            entity: {
                id: el.id
                kind: 'unit'
            }
        })
})
