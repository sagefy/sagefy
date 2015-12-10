broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .unfollow': (e, el) ->
        e.preventDefault() if e
        if window.confirm('Unfollow?')
            tasks.unfollow(el.id)

})
