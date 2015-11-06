broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    'click .unfollow': (e, el) ->
        e.preventDefault() if e
        if window.confirm('Unfollow?')
            actions.unfollow(el.id)

})
