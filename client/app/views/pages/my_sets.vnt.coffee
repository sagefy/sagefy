broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .engage-set': (e, el) ->
        e.preventDefault if e
        entityID = e.target.id
        tasks.chooseSet(entityID)
})
