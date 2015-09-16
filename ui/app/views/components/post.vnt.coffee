broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    'click .post .expand': (e, el) ->
        e.preventDefault() if e
        # TODO el
})
