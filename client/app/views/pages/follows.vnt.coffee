broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .follows__unfollow-button': (e, el) ->
        e.preventDefault() if e
        if window.confirm('Unfollow?')
            tasks.unfollow(el.id)

})
