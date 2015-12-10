broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .post .expand': (e, el) ->
        e.preventDefault() if e
        # TODO el
})
