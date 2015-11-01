broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    'click .engage-set': (e, el) ->
        e.preventDefault if e
        entityID = e.target.id
        actions.chooseSet(entityID)
})
